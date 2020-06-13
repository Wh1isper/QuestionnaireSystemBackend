from AdminBaseHandler import AdminBaseHandler, authenticated, xsrf
from orm import UserInfoTable
from orm import QuestionNaireInfoTable
import json
import time


class AdminUserStateChange(AdminBaseHandler):
    @xsrf
    @authenticated
    async def post(self, *args, **kwargs):
        # 管理员封禁/解封用户（根据email更改用户信息）
        # 接口约定： https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E7%94%A8%E6%88%B7api
        # 1. 获取post请求信息
        # 2. 确认获取信息非空
        # 3. 根据type修改state状态码
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        email = json_data.get('email')
        op_type = json_data.get('type')
        if not email:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not op_type in [0, 1]:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if op_type == 0:
            state = 0
        elif op_type == 1:
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
        # 管理员封禁/解封问卷（根据Q_ID修改问卷信息）
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E5%B0%81%E7%A6%81%E8%A7%A3%E5%B0%81%E9%97%AE%E5%8D%B7api
        # 1. 获取post请求信息
        # 2. 确认获取信息非空
        # 3. 根据type修改state状态码
        json_data = self.get_json_data()
        if not json_data:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        Q_ID = json_data.get('Q_ID')
        op_type = json_data.get('type')
        if not Q_ID:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if not op_type in [0, 1]:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if op_type == 0:
            state = 0
        elif op_type == 1:
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
        # 管理员获取用户信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E7%94%A8%E6%88%B7%E5%88%97%E8%A1%A8api
        # 1. 获取offset
        # 2. 查询数据库 获取用户信息
        # 3. 打包返回
        engine = await self.get_engine()
        try:
            offset = int(self.get_query_argument('offset', "0"))
        except ValueError:
            return self.raise_HTTP_error(403,self.MISSING_DATA)
        if offset < 0:
            return self.raise_HTTP_error(403,self.MISSING_DATA)

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
            ret_list.append(user_module)
        self.write(json.dumps(ret_list))


class AdminGetQuestionnaireList(AdminBaseHandler):
    @xsrf
    @authenticated
    async def get(self, *args, **kwargs):
        # 管理员获取问卷信息列表
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%AE%A1%E7%90%86%E5%91%98%E8%8E%B7%E5%8F%96%E9%97%AE%E5%8D%B7%E5%88%97%E8%A1%A8api
        # 1. 获取offset
        # 2. 查询问卷数据库 获取问卷信息
        # 3. 通过问卷信息里的 U_ID 查询用户信息数据库 获取用户名U_Name
        # 4. 打包返回
        engine = await self.get_engine()
        try:
            offset = int(self.get_query_argument('offset', "0"))
        except ValueError:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        if offset < 0:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        ret_list = []
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .limit(20).offset(offset))
            questionnaire_info_list = await result.fetchall()
        u_id_list = []
        ques_info_list = []
        for questionnaire_info in questionnaire_info_list:
            questionnaire_module = {
                'Q_ID': questionnaire_info.QI_ID,
                'Q_name': questionnaire_info.QI_Name,
                'user_ID': questionnaire_info.U_ID,
                'Q_creat_date': time.mktime(questionnaire_info.QI_Creat_Date.timetuple()),
                'Q_deadline_date': time.mktime(questionnaire_info.QI_Deadline_Date.timetuple()),
                'state': questionnaire_info.QI_State,
            }
            u_id_list.append(questionnaire_info.U_ID)
            ques_info_list.append(questionnaire_module)
        async with engine.acquire() as conn:
            result = await conn.execute(UserInfoTable.select()
                                        .where(UserInfoTable.c.U_ID.in_(u_id_list)))
            user_info_list = await result.fetchall()
        u_id_to_u_name_map = {}
        for user_info in user_info_list:
            u_id_to_u_name_map[user_info.U_ID] = user_info.U_Name
        for ques_info in ques_info_list:
            ques_info['user_name'] = u_id_to_u_name_map[ques_info['user_ID']]
            ret_list.append(ques_info)
        self.write(json.dumps(ret_list))


from config import *

default_handlers = [
    (r"/api/v1/admin/userStateChange/", AdminUserStateChange),
    (r"/api/v1/admin/questionnaireStateChange/", AdminQuestionnaireStateChange),
    (r"/api/v1/admin/userList/", AdminGetUserList),
    (r"/api/v1/admin/questionnaireList/", AdminGetQuestionnaireList),
]
