from BaseHandler import BaseHandler
from orm import QuestionNaireTempTable, QuestionNaireInfoTable, QuestionNaireOptionTable, QuestionNaireQuestionTable, \
    AnswerOptionTable
from typing import Text


class QuestionnaireBaseHandler(BaseHandler):
    # 请求问卷内容的基类
    def initialize(self):
        super(QuestionnaireBaseHandler, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.QUESTIONNAIRE_CANT_BE_CHANGED = 2
        self.question_map = {}
        self.option_map = {}

    async def get_questionnaire_data(self, q_id: int) -> Text:
        # 拉取问卷内容
        # !!使用前先进行用户鉴权
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireTempTable.select()
                                        .where(QuestionNaireTempTable.c.QI_ID == q_id))
            questionnaire_temp = await result.fetchone()
        return questionnaire_temp.Q_Content if questionnaire_temp else None

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

    async def get_question_content(self, qi_id, qq_id) -> Text:
        content = self.question_map.get(str(qq_id))
        if not content:
            engine = await self.get_engine()
            async with engine.acquire() as conn:
                result = await conn.execute(QuestionNaireQuestionTable.select()
                                            .where(QuestionNaireQuestionTable.c.QQ_ID == qq_id)
                                            .where(QuestionNaireQuestionTable.c.QI_ID == qi_id)
                                            )
                question_info = (await result.fetchone())
            content = question_info.QQ_Content
            self.question_map[str(qq_id)] = content
        return content

    async def get_option_content(self, qi_id, qq_id, qo_id) -> Text:
        content = self.option_map.get(str(qq_id) + ':' + str(qo_id))
        if not content:
            engine = await self.get_engine()
            async with engine.acquire() as conn:
                result = await conn.execute(QuestionNaireOptionTable.select()
                                            .where(QuestionNaireOptionTable.c.QO_ID == qo_id)
                                            .where(QuestionNaireOptionTable.c.QI_ID == qi_id)
                                            .where(QuestionNaireOptionTable.c.QQ_ID == qq_id)
                                            )
                option_info = (await result.fetchone())
            content = option_info.QO_Content
            self.option_map[str(qq_id) + ':' + str(qo_id)] = content
        return content

    async def get_option_count(self, qi_id, qq_id, qo_id) -> int:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(AnswerOptionTable.select()
                                        .where(AnswerOptionTable.c.QO_ID == qo_id)
                                        .where(AnswerOptionTable.c.QI_ID == qi_id)
                                        .where(AnswerOptionTable.c.QQ_ID == qq_id)
                                        )
            question_info = await result.fetchall()
        return len(question_info)
