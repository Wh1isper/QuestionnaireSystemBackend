from BaseHandler import BaseHandler, authenticated, xsrf
from orm import QuestionNaireInfoTable
import time
import datetime
from QuestionnaireContentHandler import QuestionnaireContentHandler


class QuestionnairePublishHandler(QuestionnaireContentHandler):
    def initialize(self):
        super(QuestionnairePublishHandler, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.BAD_END_DATE = 2

    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 发布问卷
        # 1. 验证问卷所属权
        # 2. 修改问卷信息
        # 3. 持久化存储问卷
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = json_data.get('Q_ID')
        end_date = datetime.datetime.fromtimestamp(int(json_data.get('end_date')))
        if not (q_id and end_date):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if self.valid_date_duration(end_date):
            return self.raise_HTTP_error(403, self.BAD_END_DATE)

        questionnaire_module = {
            'U_ID': self.current_user,
            'Q_ID': q_id,
            'end_date': end_date
        }

        await self.presistent_questionnaire(questionnaire_module)
        await self.publish_quesitonnaire_info(questionnaire_module)

    def valid_date_duration(self, end_date: datetime.datetime) -> bool:
        # 问卷最长1-30天
        return datetime.date.today() < end_date < datetime.date.today() + datetime.timedelta(days=30)

    async def publish_quesitonnaire_info(self, questionnaire_module: dict) -> None:
        # 这里不需要验证用户身份 之前已经验证过
        # 更新两个信息：截至日期和问卷状态
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireInfoTable.update()
                               .where(QuestionNaireInfoTable.c.QI_ID == questionnaire_module.get('Q_ID'))
                               .values(QI_Deadline_Date=questionnaire_module.get('end_date')),
                               QI_STATE=1)
            await conn._commit_impl()

    async def presistent_questionnaire(self, questionnaire_module: dict) -> None:
        # todo 持久化存储问卷
        # 1. 从暂存文件中拉取问卷内容
        # 2. 做格式化存储
        json_data = await self.get_questionnaire_data(questionnaire_module.get('Q_ID'))


class QuestionaireChangeStateHandler(BaseHandler):
    def initialize(self, state):
        super(QuestionaireChangeStateHandler, self).initialize()
        self.QUESTIONNAIRE_NOT_FOUND = 1
        self.STATE = state

    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 1. 验证问卷所属权
        # 2. 修改后问卷状态码不得变小（不得倒退）
        # 3. 修改问卷信息
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = json_data.get('Q_ID')
        if not q_id:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if self.STATE < self.get_questionnaire_state(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)

        await self.change_questionnaire_state(q_id)

    async def change_questionnaire_state(self, q_id: int) -> None:
        # 这里不需要验证用户身份 之前已经验证过
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireInfoTable.update()
                               .where(QuestionNaireInfoTable.c.QI_ID == q_id)
                               .values(QI_STATE=self.STATE))
            await conn._commit_impl()


class QuestionnaireDeleteHandler(QuestionaireChangeStateHandler):
    def initialize(self, state):
        super(QuestionnaireDeleteHandler, self).initialize(state)


class QuestionnaireInactiveHandler(QuestionaireChangeStateHandler):
    def initialize(self, state):
        super(QuestionnaireInactiveHandler, self).initialize(state)


from config import *

default_handlers = [
    (r"/api/v1/questionnairePublish/", QuestionnairePublishHandler),
    (r"/api/v1/questionnaireDelete/", QuestionnaireDeleteHandler, dict(state=3)),
    (r"/api/v1/questionnaireInactive/", QuestionnaireInactiveHandler, dict(state=2)),
]
