from BaseHandler import BaseHandler, authenticated, xsrf
from orm import QuestionNaireInfoTable, QuestionNaireOptionTable, QuestionNaireQuestionTable
import time
import datetime
from QuestionnaireBaseHandler import QuestionnaireBaseHandler
import json
from typing import List


class QuestionnairePublishHandler(QuestionnaireBaseHandler):
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
        if not await self.is_questionnaire_not_published(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not (q_id and end_date):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not await self.valid_user_questionnaire_relation(q_id):
            return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        if not self.valid_date_duration(end_date):
            return self.raise_HTTP_error(403, self.BAD_END_DATE)

        questionnaire_module = {
            'U_ID': self.current_user,
            'Q_ID': q_id,
            'end_date': end_date
        }

        if not await self.presistent_questionnaire(questionnaire_module):
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        await self.publish_quesitonnaire_info(questionnaire_module)

    def valid_date_duration(self, end_date: datetime.datetime) -> bool:
        # 问卷最长1-30天
        return datetime.datetime.today() < end_date < datetime.datetime.today() + datetime.timedelta(days=30)

    async def publish_quesitonnaire_info(self, questionnaire_module: dict) -> None:
        # 这里不需要验证用户身份 之前已经验证过
        # 更新两个信息：截至日期和问卷状态
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(
                QuestionNaireInfoTable.update()
                    .where(QuestionNaireInfoTable.c.QI_ID == questionnaire_module.get('Q_ID'))
                    .values(QI_Deadline_Date=questionnaire_module.get('end_date')), QI_STATE=1)
            await conn._commit_impl()

    async def presistent_questionnaire(self, questionnaire_module: dict) -> bool or None:
        # 持久化存储问卷
        # 1. 从暂存文件中拉取问卷内容
        # 2. 做格式化存储：分别对问题表和选项表进行插入
        # todo 日志管理 此模块失败需要记录日志
        q_id = questionnaire_module.get('Q_ID')
        try:
            # 可能存在未提交过保存的问卷
            json_data = await self.get_questionnaire_data(q_id)
        except AttributeError:
            return False
        content: List[dict] = json.loads(json_data).get('content')
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            # 创建事务
            for question in content:
                question_id = question.get('question_id')
                question_content = question.get('question_content')
                question_type = int(question.get('question_type'))
                options: List[dict] = question.get('option') if question_type == 0 or question_type == 1 else None
                # 对问题进行插入
                await conn.execute(QuestionNaireQuestionTable.insert().values(
                    QI_ID=q_id,
                    QQ_ID=question_id,
                    QQ_Type=question_type,
                    QQ_Content=question_content
                ))
                # 对选项进行插入
                if options:
                    # 单选/多选情况
                    for option in options:
                        option_id = option.get('option_id')
                        option_content = option.get('option_content')
                        await conn.execute(QuestionNaireOptionTable.insert().values(
                            QO_ID=option_id,
                            QQ_ID=question_id,
                            QI_ID=q_id,
                            QO_Type=question_type,
                            QO_Content=option_content
                        ))
                else:
                    # 填空情况
                    await conn.execute(QuestionNaireOptionTable.insert().values(
                        QO_ID=1,
                        QQ_ID=question_id,
                        QI_ID=q_id,
                        QO_Type=question_type,
                        QO_Content=None
                    ))
            # 一并提交
            await conn._commit_impl()
        return True


class QuestionaireChangeStateHandler(QuestionnaireBaseHandler):
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
        if self.STATE < await self.get_questionnaire_state(q_id):
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
