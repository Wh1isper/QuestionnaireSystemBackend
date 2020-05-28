from BaseHandler import BaseHandler, authenticated
from typing import Text


class QuestionnaireSave(BaseHandler):
    def initialize(self):
        super(QuestionnaireSave, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.QUESTIONNAIRE_CANT_BE_CHANGED = 2

    @authenticated
    async def post(self):
        # 暂存问卷，不结构化存储，仅存储前端发回的数据
        # 1. 验证问卷所属权
        # 2. 验证问卷状态
        # 3. 保存问卷
        pass

    async def save_questionnaire(self, questionnaire_save_module: dict) -> None:
        # 保存问卷
        # 需要验证json格式正确
        pass


class QuestionnaireContent(BaseHandler):
    def initialize(self):
        super(QuestionnaireSave, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.QUESTIONNAIRE_CANT_BE_CHANGED = 2

    @authenticated
    async def get(self, *args, **kwargs):
        # 拉取问卷内容，直接从暂存的信息中拉取
        # 1. 验证问卷所属权
        # 2. 验证问卷状态
        # 3. 拉取并发送
        pass

    async def get_questionnaire_data(self, q_id) -> Text:
        # 拉取问卷信息
        pass


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSave/", QuestionnaireSave),
    (r"/api/v1/questionnaireGet/", QuestionnaireContent),
]
