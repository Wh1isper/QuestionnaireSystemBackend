from db_config import *
from aiomysql.sa import create_engine
from aiomysql import create_pool


async def get_engine():
    engine = await create_engine(user=USERNAME, db=DBNAME, host=HOST, password=PASSWORD)
    return engine
