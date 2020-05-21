# 开发过程中的小测试

import asyncio

from ORM.orm import *
from aioengine import *
from sqlalchemy.sql import text
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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_query())
