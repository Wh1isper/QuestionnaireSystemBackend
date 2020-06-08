from BaseHandler import BaseHandler, xsrf
from encrypt import password_encrypt
from orm import UserInfoTable, UserPwdTable, UserLoginRecordTable
import json
import datetime
from typing import Text
from config import PASSWORD_REG, UNITTEST
import re


class RegisterHandler(BaseHandler):
    def initialize(self, pwd_salt):
        super(RegisterHandler, self).initialize()
        self.EMAIL_REPETITION = 1
        self.EMAIL_CHECK_CODE_ERROR = 2
        self.PWD_REG_CHECK_FAIL = 3
        self.PWD_SALT = pwd_salt

    @xsrf
    async def post(self, *args, **kwargs):
        # 用户注册 首先检查邮箱是否已经注册，再检查邮箱验证码和密码强度，最后写入数据库完成注册
        # 写入数据库时需要初始化三个表，按以下顺序：UserInfo、UserPwd、UserLoginRecord
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E6%B3%A8%E5%86%8Capi
        # todo 日志功能，此模块失败需要记录日志
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 参数读取
        try:
            email = json_data.get('email')
            username = json_data.get('usrname')
            birth = datetime.datetime.fromtimestamp(int(json_data.get('birth')))
            pwd = json_data.get('pwd')
            email_code = json_data.get('email_code')
            sex = int(json_data.get('sex'))
        except:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 必填项确认
        if not (email and username):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 重复注册确认
        if await self.email_is_registered(email):
            return self.raise_HTTP_error(403, self.EMAIL_REPETITION)
        # 性别0/1确认
        if not (sex == 0 or sex == 1):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 邮箱验证码确认
        if not self.valid_email_checkcode(email_code):
            return self.raise_HTTP_error(403, self.EMAIL_CHECK_CODE_ERROR)
        # 密码强度确认
        if not self.valid_pwd_reg(pwd):
            return self.raise_HTTP_error(403, self.PWD_REG_CHECK_FAIL)
        # 进入注册流程：
        usr_data_dict = {
            'email': email,
            'username': username,
            'birth': birth,
            'pwd': pwd,
            'sex': sex,
        }
        if not await self.register(usr_data_dict):
            return self.raise_HTTP_error(500)

    async def register(self, data_dict: dict) -> bool:
        # 注册流程：初始化三个表，按以下顺序：UserInfo、UserPwd、UserLoginRecord
        # 下面嵌入了三个函数
        async def register_user_info(data_dict: dict, conn) -> int:
            # 初始化用户信息并返回自增主键U_ID，途中出错返回503，由tornado接管
            await conn.execute(
                UserInfoTable.insert().values(U_Email=data_dict.get('email'),
                                              U_Name=data_dict.get('username'),
                                              U_Sex=data_dict.get('sex'),
                                              U_Birth=data_dict.get('birth'),
                                              U_State=self.USER_STATE_NORMAL))
            result = await conn.execute("select @@IDENTITY")
            u_id = (await result.fetchone())[0]
            return u_id

        async def register_user_pwd(data_dict: dict, u_id: int, conn) -> None:
            # 初始化用户密码，途中出错返回503，由tornado接管
            await conn.execute(
                UserPwdTable.insert().values(U_ID=u_id,
                                             U_Pwd=password_encrypt(data_dict.get('pwd'),
                                                                    self.PWD_SALT)))

        async def register_user_login_record(u_id: int, conn) -> None:
            # 初始化用户登录信息，途中出错返回503，由tornado接管
            await conn.execute(
                UserLoginRecordTable.insert().values(U_ID=u_id))

        # func: register
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            # 三表插入形成事务
            u_id = await register_user_info(data_dict, conn)
            if not u_id:
                return False
            await register_user_pwd(data_dict, u_id, conn)
            await register_user_login_record(u_id, conn)
            await conn._commit_impl()
        return True

    async def email_is_registered(self, email: Text) -> bool:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(UserInfoTable
                                        .select()
                                        .where(UserInfoTable.c.U_Email == email))
            usr = await result.fetchone()
        return bool(usr)

    def valid_email_checkcode(self, email_code: Text) -> bool:
        # 验证邮箱验证码 单元测试模式下无需验证
        EMAIL_CODE = self.get_str_from_secure_cookie('email_check_code')
        return UNITTEST or (EMAIL_CODE and EMAIL_CODE.strip().lower() == email_code.strip().lower())


from config import *

default_handlers = [
    (r"/api/v1/register/", RegisterHandler, dict(pwd_salt=PWD_SALT)),
]
