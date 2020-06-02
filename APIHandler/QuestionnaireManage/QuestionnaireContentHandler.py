from BaseHandler import BaseHandler, authenticated, xsrf
from typing import Text
from orm import QuestionNaireTempTable, QuestionNaireInfoTable
import json


class QuestionnaireContentHandler(BaseHandler):
    # 请求问卷内容的基类
    def initialize(self):
        super(QuestionnaireContentHandler, self).initialize()
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
        # 4. 问卷禁用 is_questionnaire_be_banned
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


class QuestionnaireSave(QuestionnaireContentHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 暂存问卷，不结构化存储，仅存储前端发回的数据
        # 1. 验证问卷所属权
        # 2. 验证问卷状态：未发布
        # 3. 保存问卷
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = json_data.get('Q_ID')
        if not q_id:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_content = json_data
        if not await self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not self.is_questionnaire_not_published(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_CANT_BE_CHANGED)
        questionnaire_save_module = {
            'Q_ID': q_id,
            'Q_Content': q_content,
        }
        if not await self.save_questionnaire(questionnaire_save_module):
            return self.raise_HTTP_error(403, self.MISSING_DATA)

    async def save_questionnaire(self, questionnaire_save_module: dict) -> bool:
        # 存入数据库
        # todo 数据校验 P2
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireTempTable.update()
                               .where(QuestionNaireTempTable.c.QI_ID == questionnaire_save_module.get('Q_ID'))
                               .values(Q_Content=questionnaire_save_module.get('Q_Content')))
            await conn._commit_impl()
        return True


class QuestionnaireContent(QuestionnaireContentHandler):
    @authenticated
    async def get(self, *args, **kwargs):
        # 拉取问卷内容，直接从暂存的信息中拉取
        # 1. 验证问卷状态
        #   a. 未发布：仅所有者可查看
        #   b. 停用、已发布：所有人均可查看
        #   c. 禁用/删除：所有人均不可查看（管理员除外）
        # 2. 拉取并返回
        try:
            q_id = int(self.get_query_argument('Q_ID'))
        except ValueError:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not q_id:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if await self._not_publish(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if await self.is_questionnaire_be_banned(q_id) and not self.is_current_user_admin():
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        content = await self.get_questionnaire_data(q_id)
        self.write(content)

    async def _not_publish(self, q_id: int) -> bool:
        return await self.is_questionnaire_not_published(q_id) and not await self.valid_user_questionnaire_relation(
            q_id)

    def is_current_user_admin(self) -> bool:
        return bool(self.get_secure_cookie('admin'))


from config import *

default_handlers = [
    (r"/api/v1/questionnaireSave/", QuestionnaireSave),
    (r"/api/v1/questionnaireGet/", QuestionnaireContent),
]
