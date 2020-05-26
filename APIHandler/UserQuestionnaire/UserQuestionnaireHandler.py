from BaseHandler import BaseHandler, authenticated
from orm import QuestionNaireInfoTable
from typing import Text
import json
import datetime
from config import DEBUG


class UserQuestionnaireListHandler(BaseHandler):
    @authenticated
    async def get(self, *args, **kwargs):
        # 获取当前用户问卷列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E9%97%AE%E5%8D%B7%E5%88%97%E8%A1%A8api
        # 1. 获取用户id:self.current_user
        # 2. 查询数据库 获取用户id下的问卷信息
        # 3. 打包返回
        pass




default_handlers = [
    (r"/api/v1/userQuestionnaireList/", UserQuestionnaireListHandler),
]
