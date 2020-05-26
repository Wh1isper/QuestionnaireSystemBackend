from BaseHandler import BaseHandler, authenticated
from orm import UserInfoTable, UserPwdTable
import json
import datetime
from typing import Text
from encrypt import password_encrypt


class UserInfoHandler(BaseHandler):
    @authenticated
    async def post(self, *args, **kwargs):
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
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
    def initialize(self, pwd_sault):
        super(UserChangePwdHandler, self).initialize()
        self.OLDPWD_ERROR = 1
        self.PWD_REG_CHECK_FAIL = 2
        self.PWD_SAULT = pwd_sault

    @authenticated
    async def post(self, *args, **kwargs):
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        old_pwd = json_data.get('old_pwd')
        pwd = json_data.get('pwd')

        if not (old_pwd and pwd):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not await self.valid_pwd(old_pwd):
            return self.raise_HTTP_error(403, self.OLDPWD_ERROR)
        if not self.valid_pwd(pwd):
            return self.raise_HTTP_error(403, self.PWD_REG_CHECK_FAIL)
        await self.update_pwd(pwd)

    async def update_pwd(self, pwd: Text) -> None:
        engine = await self.get_engine()
        secure_pwd = password_encrypt(pwd, self.PWD_SAULT)
        async with engine.acquire() as conn:
            await conn.execute(UserPwdTable.update()
                               .where(UserPwdTable.c.U_ID == self.current_user)
                               .values(U_Pwd=secure_pwd))

    async def valid_pwd(self, pwd: Text) -> bool:
        engine = await self.get_engine()
        secure_pwd = password_encrypt(pwd, self.PWD_SAULT)
        async with engine.acquire() as conn:
            result = await conn.execute(UserPwdTable.select()
                                        .where(UserPwdTable.c.U_ID == self.current_user)
                                        .where(UserPwdTable.c.U_Pwd == secure_pwd))
            userinfo = await result.fetchone()
            return bool(userinfo)


from config import *

default_handlers = [
    (r"/api/v1/userInfo/", UserInfoHandler),
    (r"/api/v1/changePwd/", UserChangePwdHandler, dict(pwd_sault=PWD_SAULT))
]
