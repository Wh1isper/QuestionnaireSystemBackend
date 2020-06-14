from QuestionnaireBaseHandler import QuestionnaireBaseHandler
from BaseHandler import xsrf
from orm import QuestionNaireInfoTable, UserInfoTable
import time


class QuestionnaireInfoHandler(QuestionnaireBaseHandler):
    @xsrf
    async def get(self):
        # 获取问卷信息
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E9%97%AE%E5%8D%B7%E4%BF%A1%E6%81%AFapi
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
        if not self.is_current_user_admin():
            if await self._not_publish(q_id):
                # 没有发布且不是拥有者：拒绝访问
                return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
            if await self.is_questionnaire_be_banned(q_id):
                # 被删除/禁用：拒绝访问
                return self.raise_HTTP_error(403, self.QUESTIONNAIRE_NOT_FOUND)
        questionnaire_info = await self.get_questionnaire_info(q_id)
        self.write(questionnaire_info)

    async def _not_publish(self, q_id: int) -> bool:
        return await self.is_questionnaire_not_published(q_id) and not await self.valid_user_questionnaire_relation(
            q_id)

    def is_current_user_admin(self) -> bool:
        return bool(self.get_secure_cookie('admin'))

    async def get_questionnaire_info(self, q_id: int) -> dict:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id))
            questionnaire_info = await result.fetchone()
            result = await conn.execute(UserInfoTable.select().where(UserInfoTable.c.U_ID == questionnaire_info.U_ID))
            user_info = await result.fetchone()
            u_name = user_info.U_Name

        questionnaire_module = {
            'Q_Name': questionnaire_info.QI_Name,
            'Q_Create_Date': self.datetime_to_timestamp(questionnaire_info.QI_Creat_Date),
            'Q_Deadline_Date': self.datetime_to_timestamp(questionnaire_info.QI_Deadline_Date),
            'U_Name': u_name,
            'state': questionnaire_info.QI_State,
        }
        return questionnaire_module


from config import *

default_handlers = [
    (r"/api/v1/questionnaireInfo/", QuestionnaireInfoHandler),
]
