from BaseHandler import BaseHandler
from typing import Text
import json
from orm import UserInfoTable, UserPwdTable, UserLoginRecordTable
from encrypt import password_encrypt
import datetime
from config import UNITTEST


class LoginHandler(BaseHandler):
    def initialize(self, pwd_salt):
        super(LoginHandler, self).initialize()
        self.USER_PWD_ERROR = 1
        self.CHECK_CODE_ERROR = 2
        self.PWD_SALT = pwd_salt

    async def post(self, *args, **kwargs):
        # 获取post请求数据 访问数据库进行用户验证并记录登录
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E7%99%BB%E5%BD%95api
        # 成功将set-cookie:user 存有加密后的用户id
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        email = json_data.get('email')
        pwd = json_data.get('pwd')
        check_code = json_data.get('check_code')
        if not (email and pwd and check_code):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not self.valid_checkcode(check_code):
            return self.raise_HTTP_error(403, self.CHECK_CODE_ERROR)
        user_id = await self.valid_user(email, pwd)
        if not user_id:
            return self.raise_HTTP_error(403, self.USER_PWD_ERROR)
        await self.login_record(user_id)
        self.set_secure_cookie("user", user_id, expires_days=1)

    def valid_checkcode(self, check_code: Text) -> bool:
        # 验证码 单元测试模式下无需验证
        CHECK_CODE = self.get_secure_cookie("check_code")
        return UNITTEST or (CHECK_CODE and CHECK_CODE.strip().lower() == check_code.strip().lower())

    async def valid_user(self, email: Text, pwd: Text) -> Text or None:
        # 验证用户
        # 第一步验证邮箱是否注册，返回用户ID
        # 第二步验证用户ID与密码是否对应
        async def valid_email(email: Text) -> Text or None:
            engine = await self.get_engine()
            async with engine.acquire() as conn:
                result = await conn.execute(UserInfoTable.select().where(UserInfoTable.c.U_Email == email))
                userinfo = await result.fetchone()
            if userinfo:
                return userinfo.U_ID
            else:
                return None

        async def valid_pwd(uid: Text, pwd: Text) -> bool:
            engine = await self.get_engine()
            secure_pwd = password_encrypt(pwd, self.PWD_SALT)
            async with engine.acquire() as conn:
                result = await conn.execute(UserPwdTable.select()
                                            .where(UserPwdTable.c.U_ID == u_id)
                                            .where(UserPwdTable.c.U_Pwd == secure_pwd))
                userinfo = await result.fetchone()
                print()
            return bool(userinfo)

        u_id = await valid_email(email)
        if not u_id:
            return None
        isvalid = await valid_pwd(u_id, pwd)
        if not isvalid:
            return None
        return str(u_id)

    async def login_record(self, user_id: Text) -> None:
        ip = self.request.remote_ip
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(
                UserLoginRecordTable.update().
                    where(UserLoginRecordTable.c.U_ID == user_id).
                    values(U_Login_Date=datetime.datetime.today(), U_Login_IP=ip)
            )
            # aiomysql bug .commit()方法不存在
            # 这里直接调用实现即可 or conn.execute('commit')
            await conn._commit_impl()


class LogoutHandler(BaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('user')


from config import *

default_handlers = [
    (r"/api/v1/login/", LoginHandler, dict(pwd_salt=PWD_SALT)),
    (r"/api/v1/logout/", LogoutHandler),
]
