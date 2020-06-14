from BaseHandler import BaseHandler, authenticated, xsrf
from orm import QuestionNaireTempTable, QuestionNaireInfoTable
import json
from QuestionnaireBaseHandler import QuestionnaireBaseHandler


class QuestionnaireSaveHandler(QuestionnaireBaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 暂存问卷，不结构化存储，仅存储前端发回的数据
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E9%97%AE%E5%8D%B7%E4%BF%9D%E5%AD%98api
        # 1. 验证问卷所属权
        # 2. 验证问卷状态：未发布
        # 3. 保存问卷
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = json_data.get('Q_ID')
        if not q_id:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not await self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not await self.is_questionnaire_not_published(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_CANT_BE_CHANGED)
        # 转字符串存储
        q_content = json.dumps(json_data)
        questionnaire_save_module = {
            'Q_ID': q_id,
            'Q_Content': q_content,
        }
        if not await self.save_questionnaire(questionnaire_save_module):
            return self.raise_HTTP_error(403, self.MISSING_DATA)

    async def save_questionnaire(self, questionnaire_save_module: dict) -> bool:
        # 存入数据库
        # 不进行数据校验，存在性能风险
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireTempTable.update()
                               .where(QuestionNaireTempTable.c.QI_ID == questionnaire_save_module.get('Q_ID'))
                               .values(Q_Content=questionnaire_save_module.get('Q_Content')))
            await conn._commit_impl()
        return True


class QuestionnaireContentHandler(QuestionnaireBaseHandler):
    @xsrf
    async def get(self, *args, **kwargs):
        # 拉取问卷内容，直接从暂存的信息中拉取
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E9%97%AE%E5%8D%B7%E5%86%85%E5%AE%B9%E8%8E%B7%E5%8F%96api
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
    (r"/api/v1/questionnaireSave/", QuestionnaireSaveHandler),
    (r"/api/v1/questionnaireGet/", QuestionnaireContentHandler),
]
