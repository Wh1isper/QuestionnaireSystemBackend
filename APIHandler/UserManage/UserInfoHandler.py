from BaseHandler import BaseHandler, authenticated, xsrf
from orm import UserInfoTable, UserPwdTable
import json
import datetime
from typing import Text
from encrypt import password_encrypt
import time


class UserInfoHandler(BaseHandler):
    @authenticated
    async def get(self, *args, **kwargs):
        # 获取用户信息
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E8%8E%B7%E5%8F%96api
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(UserInfoTable.select()
                                        .where(UserInfoTable.c.U_ID == self.current_user))
            user_info = await result.fetchone()
        birth = self.datetime_to_timestamp(user_info.U_Birth)
        user_module = {
            "email": user_info.U_Email,
            "usrname": user_info.U_Name,
            "sex": user_info.U_Sex,
            "birth": birth,
            "state": user_info.U_State,
        }
        self.write(user_module)

    @authenticated
    async def post(self, *args, **kwargs):
        # 修改用户信息
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF%E4%BF%AE%E6%94%B9api
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        try:
            username = json_data.get('usrname')
            birth = datetime.datetime.fromtimestamp(int(json_data.get('birth')))
            sex = json_data.get('sex')
        except:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        user_info_dict = {
            'U_ID': self.current_user,
            'username': username,
            'birth': birth,
            'sex': sex,
        }
        await self.update_user_info(user_info_dict)

    async def update_user_info(self, data_dict: dict) -> None:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(
                UserInfoTable.update().
                    where(UserInfoTable.c.U_ID == data_dict.get('U_ID')).
                    values(U_Name=data_dict.get('username'),
                           U_Sex=data_dict.get('sex'),
                           U_Birth=data_dict.get('birth'))
            )
            # aiomysql bug .commit()方法不存在
            # 这里直接调用实现即可 or conn.execute('commit')
            await conn._commit_impl()


class UserChangePwdHandler(BaseHandler):
    def initialize(self, pwd_salt):
        super(UserChangePwdHandler, self).initialize()
        self.OLDPWD_ERROR = 1
        self.PWD_REG_CHECK_FAIL = 2
        self.PWD_SALT = pwd_salt

    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 验证密码成功后修改用户密码
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        old_pwd = json_data.get('old_pwd')
        pwd = json_data.get('pwd')
        # 必填项确认
        if not (old_pwd and pwd):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 验证密码
        if not await self.valid_pwd(old_pwd):
            return self.raise_HTTP_error(403, self.OLDPWD_ERROR)
        # 验证新密码强度
        if not self.valid_pwd_reg(pwd):
            return self.raise_HTTP_error(403, self.PWD_REG_CHECK_FAIL)
        # 更新密码
        await self.update_pwd(pwd)

    async def update_pwd(self, pwd: Text) -> None:
        engine = await self.get_engine()
        secure_pwd = password_encrypt(pwd, self.PWD_SALT)
        async with engine.acquire() as conn:
            await conn.execute(UserPwdTable.update()
                               .where(UserPwdTable.c.U_ID == self.current_user)
                               .values(U_Pwd=secure_pwd))
            await conn._commit_impl()

    async def valid_pwd(self, pwd: Text) -> bool:
        engine = await self.get_engine()
        secure_pwd = password_encrypt(pwd, self.PWD_SALT)
        async with engine.acquire() as conn:
            result = await conn.execute(UserPwdTable.select()
                                        .where(UserPwdTable.c.U_ID == self.current_user)
                                        .where(UserPwdTable.c.U_Pwd == secure_pwd))
            userinfo = await result.fetchone()
        return bool(userinfo)


from config import *

default_handlers = [
    (r"/api/v1/userInfo/", UserInfoHandler),
    (r"/api/v1/changePwd/", UserChangePwdHandler, dict(pwd_salt=PWD_SALT))
]
