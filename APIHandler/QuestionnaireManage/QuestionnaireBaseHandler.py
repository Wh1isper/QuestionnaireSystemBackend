from BaseHandler import BaseHandler
from orm import QuestionNaireTempTable, QuestionNaireInfoTable
from typing import Text


class QuestionnaireBaseHandler(BaseHandler):
    # 请求问卷内容的基类
    def initialize(self):
        super(QuestionnaireBaseHandler, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.QUESTIONNAIRE_CANT_BE_CHANGED = 2

    async def get_questionnaire_data(self, q_id: int) -> Text:
        # 拉取问卷内容
        # !!使用前先进行用户鉴权
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireTempTable.select()
                                        .where(QuestionNaireTempTable.c.QI_ID == q_id))
            questionnaire_temp = await result.fetchone()
        return questionnaire_temp.Q_Content

    async def _valid_questionnaire_state(self, q_id: int, expect_state: int) -> bool:
        # 验证问卷状态
        # 使用以下api快速访问：
        # 1. 问卷未发布 is_questionnaire_not_published()
        # 2. 问卷已发布 is_questionnaire_published()
        # 3. 问卷停用 is_questionnaire_inactivate()
        # 4. 问卷禁用 is_questionnaire_be_banned()
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id)
                                        .where(QuestionNaireInfoTable.c.QI_State == expect_state))
            questionnaire_info = await result.fetchone()
        return bool(questionnaire_info)

    async def is_questionnaire_not_published(self, q_id: int) -> bool:
        return await self._valid_questionnaire_state(q_id, 0)

    async def is_questionnaire_published(self, q_id: int) -> bool:
        return await self._valid_questionnaire_state(q_id, 1)

    async def is_questionnaire_inactivate(self, q_id: int) -> bool:
        return await self._valid_questionnaire_state(q_id, 2)

    async def is_questionnaire_be_banned(self, q_id: int) -> bool:
        return await self._valid_questionnaire_state(q_id, 3)
