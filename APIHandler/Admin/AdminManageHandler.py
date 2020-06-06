from AdminBaseHandler import AdminBaseHandler, authenticated, xsrf
from orm import UserInfoTable
from orm import QuestionNaireInfoTable
import json


class AdminUserStateChange(AdminBaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # todo 管理员封禁/解封用户（根据email更改用户信息）
        # 接口约定： https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E7%94%A8%E6%88%B7api
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        email = json_data.get('email')
        type = json_data.get('type')
        if type == 0:
            state = 0
        elif type == 1:
            state = 1
        # 更新状态
        await self.update_state(email, state)

    async def update_state(self, email, state: int) -> None:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(UserInfoTable.update()
                               .where(UserInfoTable.c.U_Email == email)
                               .values(U_State=state))
            await conn._commit_impl()


class AdminQuestionnaireStateChange(AdminBaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # todo 管理员封禁/解封问卷（根据Q_ID修改问卷信息）
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E9%97%AE%E5%8D%B7api
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        Q_ID = json_data.get('Q_ID')
        type = json_data.get('type')
        if type == 0:
            state = 0
        elif type == 1:
            state = 3
        # 更新状态
        await self.update_state(Q_ID, state)

    async def update_state(self, Q_ID, state: int) -> None:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(QuestionNaireInfoTable.update()
                               .where(QuestionNaireInfoTable.c.QI_ID == Q_ID)
                               .values(QI_State=state))
            await conn._commit_impl()


class AdminGetUserList(AdminBaseHandler):
    @xsrf
    @authenticated
    async def get(self, *args, **kwargs):
        # todo 管理员获取用户信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E7%94%A8%E6%88%B7%E5%88%97%E8%A1%A8api
        engine = await self.get_engine()
        offset = self.get_argument('offset', '')
        ret_list = []
        async with engine.acquire() as conn:
            result = await conn.execute(UserInfoTable.select()
                                        .limit(20).offset(offset))
            user_info_list = await result.fetchall()
        for user_info in user_info_list:
            user_module = {
                "username": user_info.U_Name,
                "email": user_info.U_Email,
                "state": user_info.U_State,
            }
            ret_list.append(json.dumps(user_module))
        self.write(str(ret_list))


class AdminGetQuestionnaireList(AdminBaseHandler):
    @xsrf
    @authenticated
    async def get(self, *args, **kwargs):
        # todo 管理员获取问卷信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E9%97%AE%E5%8D%B7%E5%88%97%E8%A1%A8api
        engine = await self.get_engine()
        offset = self.get_argument('offset', '')
        ret_list = []
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .limit(20).offset(offset))
            questionnaire_info_list = await result.fetchall()
        for questionnaire_info in questionnaire_info_list:
            questionnaire_module = {
                'Q_ID': questionnaire_info.QI_ID,
                'Q_name': questionnaire_info.QI_Name,
                'user_ID': questionnaire_info.U_ID,
                'user_name': questionnaire_info.U_Name,
                'Q_creat_date': questionnaire_info.QI_Creat_Date,
                'Q_publish_date': questionnaire_info.QI_Publish_Date,
                'state': questionnaire_info.QI_State,
            }
            ret_list.append(json.dumps(questionnaire_module))
        self.write(str(ret_list))


from config import *

default_handlers = [
    (r"/api/v1/admin/userStateChange/", AdminUserStateChange),
    (r"/api/v1/admin/questionnaireStateChange/", AdminQuestionnaireStateChange),
    (r"/api/v1/admin/userList/", AdminGetUserList),
    (r"/api/v1/admin/questionnaireList/", AdminGetQuestionnaireList),
]
