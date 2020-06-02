from BaseHandler import BaseHandler, authenticated, xsrf
from orm import QuestionNaireInfoTable, QuestionNaireTempTable
import datetime
from typing import Text


class QuestionnaireCreateHandler(BaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 问卷创建
        # 1. 获取问卷标题
        # 2. 初始化问卷信息表QuestionNaireInfo, 问卷暂存表QuestionNaireTempTable
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
                                                       QI_State=0,
                                                       QI_Limit_Type=0))
            result = await conn.execute("select @@IDENTITY")
            q_id = (await result.fetchone())[0]
            await conn.execute(
                QuestionNaireTempTable.insert().values(QI_ID=q_id))
            await conn._commit_impl()
        return q_id


from config import *

default_handlers = [
    (r"/api/v1/questionnaireCreate/", QuestionnaireCreateHandler),
]
