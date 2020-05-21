from BaseHandler import BaseHandler
from tornado.web import ErrorHandler
from tornado.gen import coroutine
from typing import Text
import json
from aioengine import get_engine
from orm import UserInfoTable, UserPwdTable
from sqlalchemy.sql import text
import aiomysql
from source.encrypt import password_encrypt


class LoginHandler(BaseHandler):
    def initialize(self, pwd_sault):
        BaseHandler.initialize(self)
        self.USER_PWD_ERROR = 1
        self.CHECK_CODE_ERROR = 2
        self.PWD_SAULT = pwd_sault

    async def post(self, *args, **kwargs):
        # 获取post请求数据 访问数据库进行用户验证
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95api
        # 成功将set-cookie:user 存有加密后的用户id
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return self.raise_error(401, self.MISSING_DATA)
        email = json_data.get('email')
        pwd = json_data.get('pwd')
        check_code = json_data.get('check_code')
        if not (email and pwd and check_code):
            return self.raise_error(403, self.MISSING_DATA)
        if not self.valid_checkcode(check_code):
            return self.raise_error(403, self.CHECK_CODE_ERROR)
        user_id = await self.valid_user(email, pwd)
        if not user_id:
            return self.raise_error(403, self.USER_PWD_ERROR)
        self.set_secure_cookie("user", user_id, expires_days=1)
        self.set_status(200)

    def valid_checkcode(self, check_code: Text) -> bool:
        return self.get_secure_cookie("check_code").strip().lower() == check_code.strip().lower()

    async def valid_user(self, email: Text, pwd: Text) -> Text or None:
        async def valid_email(email: Text, engine) -> Text or None:
            async with engine.acquire() as conn:
                result = await conn.execute(UserInfoTable.select().where(text('U_Email = {}'.format(email))))
                userinfo = await result.fetchone()
                if userinfo:
                    return userinfo.U_ID
                else:
                    return None

        async def valid_pwd(uid: Text, pwd: Text, engine) -> bool:
            secure_pwd = password_encrypt(pwd, self.PWD_SAULT)
            async with engine.acquire() as conn:
                result = await conn.execute(UserPwdTable.select()
                                            .where(text('U_ID = {}'.format(uid)))
                                            .where(text('U_PWD= {}'.format(secure_pwd))))
                userinfo = await result.fetchone()
                return bool(userinfo)

        engine = await get_engine()
        u_id = await valid_email(email, engine)
        if not u_id:
            return None
        isvalid = await valid_pwd(u_id, pwd, engine)
        if not isvalid:
            return None
        return u_id


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('user')
        self.set_status(200)