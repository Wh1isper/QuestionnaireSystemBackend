from BaseHandler import BaseHandler
from encrypt import password_encrypt
from orm import UserInfoTable, UserPwdTable, UserLoginRecordTable


class RegisterHandler(BaseHandler):
    def initialize(self, pwd_sault):
        BaseHandler.initialize(self)
        self.EMAIL_REPETITION = 1
        self.EMAIL_CHECK_CODE_ERROR = 2
        # 直接使用接口注册/批量注册，可能出现密码强度不够
        self.PSSAWRD_CHECK_FAIL = 3
        self.PWD_SAULT = pwd_sault

    async def post(self, *args, **kwargs):
        # todo 用户注册 首先检查邮箱是否已经注册，再检查邮箱验证码和密码规范，最后写入数据库完成注册
        # 写入数据库时需要初始化三个表，按以下顺序：UserInfo、UserPwd、UserLoginRecord
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E6%B3%A8%E5%86%8Capi
        pass


from config import *

default_handlers = [
    (r"/api/v1/register/", RegisterHandler, dict(pwd_sault=PWD_SAULT)),
]
