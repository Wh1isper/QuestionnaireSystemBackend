from BaseHandler import BaseHandler, authenticated
from typing import Text
import json
import datetime
from config import DEBUG


class QuestionnaireRename(BaseHandler):
    def initialize(self):
        super(QuestionnaireRename, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1

    @authenticated
    async def post(self, *args, **kwargs):
        # 修改问卷名
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E4%BF%AE%E6%94%B9%E9%97%AE%E5%8D%B7%E5%90%8Dapi
        # 1. 用户鉴权 确定是问卷的拥有者
        # 2. 根据问卷ID直接修改
        pass


default_handlers = [
    (r"/api/v1/questionnaireRename/", QuestionnaireRename),
]
