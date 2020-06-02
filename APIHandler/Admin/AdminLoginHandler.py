from AdminBaseHandler import AdminBaseHandler, authenticated, xsrf


class AdminLoginHandler(AdminBaseHandler):
    def initialize(self, pwd_salt):
        self.PWD_SALT = pwd_salt

    @xsrf
    def post(self, *args, **kwargs):
        # todo 管理员登录功能，cookie为关闭浏览器即删除
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E7%99%BB%E5%BD%95api
        pass


class AdminLogoutHandler(AdminBaseHandler):
    def get(self, *args, **kwargs):
        self.clear_cookie('admin')


from config import *

default_handlers = [
    (r"/api/v1/admin/login/", AdminLoginHandler, dict(pwd_salt=PWD_SALT)),
    (r"/api/v1/admin/logout/", AdminLogoutHandler),
]
