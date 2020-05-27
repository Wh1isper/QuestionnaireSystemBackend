# 开发过程中的小测试

import asyncio

from ORM.orm import *
from aioengine import *
from sqlalchemy.sql import text
import datetime
import json

async def test_table_orm():
    engine = await get_engine()
    async with engine.acquire() as conn:
        for i in [UserInfoTable,
                  UserPwdTable,
                  UserLoginRecordTable,
                  QuestionNaireInfoTable,
                  QuestionNaireQuestionTable,
                  QuestionNaireOptionTable,
                  QuestionNaireTempTable,
                  AnswerOptionTable]:
            x = await conn.execute(i.select())
            ret = await x.fetchall()
            print(ret)
    engine.close()
    await engine.wait_closed()


async def test_query():
    ret_list = []
    engine = await get_engine()
    async with engine.acquire() as conn:
        result = await conn.execute(QuestionNaireInfoTable.select()
                                    .where(QuestionNaireInfoTable.c.U_ID == 3))
        questionnaire_info_list = await result.fetchall()
    for questionnaire_info in questionnaire_info_list:
        info_module = {
            "Q_ID": questionnaire_info.QI_ID,
            "Q_Name": questionnaire_info.QI_Name,
            "Q_creat_date": time.mktime(questionnaire_info.QI_Creat_Date.timetuple()),
            "Q_deadline_date": time.mktime(questionnaire_info.QI_Deadline_Date.timetuple()),
            "state": questionnaire_info.QI_State,
        }
        ret_list.append(json.dumps(info_module))
    print(ret_list)

import time


async def login_record(user_id=1):
    ip = 1
    engine = await get_engine()
    async with engine.acquire() as conn:
        await conn.execute(
            UserLoginRecordTable.update().
                where(UserLoginRecordTable.c.U_ID == user_id).
                values(U_Login_Date=datetime.datetime.today(), U_Login_IP=ip)
        )
        await conn._commit_impl()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_query())
