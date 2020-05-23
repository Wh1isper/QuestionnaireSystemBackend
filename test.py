# 开发过程中的小测试

import asyncio

from ORM.orm import *
from aioengine import *
from sqlalchemy.sql import text
import datetime

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
    engine = await get_engine()
    async with engine.acquire() as conn:
        result = await conn.execute(UserInfoTable.select().where(text('U_NAME = \'111\'')))
        print(UserInfoTable.select().where(text('U_NAME = 111')))
        userinfo = await result.fetchone()
        print(userinfo)


import time


async def login_record(user_id=1):
    ip = 1
    engine = await get_engine()
    async with engine.acquire() as conn:
        await conn.execute(
            UserLoginRecordTable.update().
                where(UserLoginRecordTable.c.U_ID == user_id).
                values(U_Login_Date=datetime.date.today(), U_Login_IP=ip)
        )
        await conn._commit_impl()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_record())
