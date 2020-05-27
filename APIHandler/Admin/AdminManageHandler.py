from AdminBaseHandler import AdminBaseHandler
from BaseHandler import authenticated


class AdminUserStateChange(AdminBaseHandler):
    @authenticated
    async def post(self, *args, **kwargs):
        # todo 管理员封禁/解封用户（根据email更改用户信息）
        # 接口约定： https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E7%94%A8%E6%88%B7api
        pass

class AdminQuestionnaireStateChange(AdminBaseHandler):
    @authenticated
    async def post(self, *args, **kwargs):
        # todo 管理员封禁/解封问卷（根据Q_ID修改问卷信息）
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E9%97%AE%E5%8D%B7api
        pass

class AdminGetUserList(AdminBaseHandler):
    @authenticated
    async def get(self,*args,**kwargs):
        # todo 管理员获取用户信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E7%94%A8%E6%88%B7%E5%88%97%E8%A1%A8api
        pass

class AdminGetQuestionnaireList(AdminBaseHandler):
    @authenticated
    async def get(self,*args,**kwargs):
        # todo 管理员获取问卷信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E9%97%AE%E5%8D%B7%E5%88%97%E8%A1%A8api
        pass


from config import *

default_handlers = [
    (r"/api/v1/admin/userStateChange/", AdminUserStateChange),
    (r"/api/v1/admin/questionnaireStateChange/", AdminQuestionnaireStateChange),
    (r"/api/v1/admin/userList/", AdminGetUserList),
    (r"/api/v1/admin/questionnaireList/", AdminGetQuestionnaireList),
]
