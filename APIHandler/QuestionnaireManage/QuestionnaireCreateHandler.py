from BaseHandler import authenticated, xsrf
from orm import QuestionNaireInfoTable, QuestionNaireTempTable, AnswerRecorderTable
import datetime
from typing import Text
from QuestionnaireBaseHandler import QuestionnaireBaseHandler


class QuestionnaireCreateHandler(QuestionnaireBaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 问卷创建
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E9%97%AE%E5%8D%B7%E5%88%9B%E5%BB%BAapi
        # 1. 获取问卷标题
        # 2. 初始化问卷信息表QuestionNaireInfo, 问卷暂存表QuestionNaireTempTable, 答卷信息表AnswerRecorderTable
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        title = json_data.get('Q_title')
        if not title:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        q_id = await self.questionnaire_create(title)
        self.write({'Q_ID': q_id})

    async def questionnaire_create(self, title: Text) -> Text:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(
                QuestionNaireInfoTable.insert().values(QI_Name=title,
                                                       U_ID=self.current_user,
                                                       QI_Creat_Date=datetime.datetime.today(),
                                                       QI_State=self.Q_STATE_UNPUBLISH,
                                                       QI_Limit_Type=0))
            result = await conn.execute("select @@IDENTITY")
            q_id = (await result.fetchone())[0]
            await conn.execute(
                QuestionNaireTempTable.insert().values(QI_ID=q_id))
            await conn.execute(
                AnswerRecorderTable.insert().values(QI_ID=q_id, Count=0))
            await conn._commit_impl()
        return q_id


from config import *

default_handlers = [
    (r"/api/v1/questionnaireCreate/", QuestionnaireCreateHandler),
]
