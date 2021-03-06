from AdminBaseHandler import AdminBaseHandler
from typing import Text
from encrypt import password_encrypt
from config import PWD_SALT
from AdminBaseHandler import AdminBaseHandler, authenticated, xsrf


class AdminLoginHandler(AdminBaseHandler):
    def initialize(self, pwd_salt):
        super(AdminLoginHandler, self).initialize()
        self.PWD_SALT = pwd_salt
        self.USER_PWD_ERROR = 1

    @xsrf
    async def post(self, *args, **kwargs):
        # 管理员登录功能，cookie为关闭浏览器即删除
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E7%99%BB%E5%BD%95api
        # 1. 获取输入的管理员账号密码
        # 2. 根据本地文件鉴权，见：config.py
        # 3. 发放权限
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        admin = json_data.get('admin')
        pwd = json_data.get('pwd')
        # 必填项确认
        if not (admin and pwd):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        # 用户鉴权
        user_id = self.valid_user(admin, pwd)
        if not user_id:
            return self.raise_HTTP_error(403, self.USER_PWD_ERROR)
        # 发放权限,浏览器关闭cookie就过期
        self.set_secure_cookie("admin", user_id, expires_days=None)

    def valid_user(self, admin: Text, pwd: Text) -> Text or None:
        # 验证用户
        # 第一步验证账号是否是admin账号
        # 第二步验证密码是否正确
        def valid_admin(admin: Text) -> Text or None:
            if admin == ADMIN_ACOUNT:
                return admin
            else:
                return None

        def valid_pwd(pwd: Text) -> bool:
            secure_pwd = password_encrypt(pwd, self.PWD_SALT)
            if secure_pwd == ADMIN_PASSWORD:
                return True
            else:
                return False
        admin_id = valid_admin(admin)
        if not admin_id:
            return None
        isvalid = valid_pwd(pwd)
        if not isvalid:
            return None
        return str(admin_id)


class AdminLogoutHandler(AdminBaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('admin')


from config import *

default_handlers = [
    (r"/api/v1/admin/login/", AdminLoginHandler, dict(pwd_salt=PWD_SALT)),
    (r"/api/v1/admin/logout/", AdminLogoutHandler),
]
