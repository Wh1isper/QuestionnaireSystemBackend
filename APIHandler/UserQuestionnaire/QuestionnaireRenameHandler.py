from BaseHandler import BaseHandler, authenticated
from typing import Text
import json
import datetime
from config import DEBUG
from orm import QuestionNaireInfoTable


class QuestionnaireRename(BaseHandler):
    def initialize(self):
        super(QuestionnaireRename, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1

    @authenticated
    async def post(self, *args, **kwargs):
        # 修改问卷名
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%94%A8%E6%88%B7%E4%BF%AE%E6%94%B9%E9%97%AE%E5%8D%B7%E5%90%8Dapi
        # 1. 用户鉴权 确定是问卷的拥有者
        # 2. 确定问卷于未发布状态(state=0)
        # 3. 根据问卷ID直接修改
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = json_data.get('Q_ID')
        q_name = json_data.get('Q_Name')
        if not (q_id and q_name):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if await self.get_questionnaire_state(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not await self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        await self.update_questionnaire_name(q_id, q_name)

    async def update_questionnaire_name(self, q_id: int, new_name: Text) -> None:
        # 更新问卷名
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireInfoTable.update()
                               .where(QuestionNaireInfoTable.c.QI_ID == q_id)
                               .values(QI_Name=new_name))
            await conn._commit_impl()


default_handlers = [
    (r"/api/v1/questionnaireRename/", QuestionnaireRename),
]
