# 开发过程中的小测试

import asyncio

from ORM.orm import *


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


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_table_orm())
