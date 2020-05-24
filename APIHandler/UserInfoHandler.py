from BaseHandler import BaseHandler, authenticated
from orm import UserInfoTable
import json
import datetime


class UserInfoHandler(BaseHandler):
    @authenticated
    async def post(self, *args, **kwargs):
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        try:
            username = json_data.get('usrname')
            birth = datetime.datetime.fromtimestamp(int(json_data.get('birth')))
            sex = json_data.get('sex')
        except:
            return self.raise_HTTP_error(403, self.MISSING_DATA)
        user_info_dict = {
            'U_ID': self.current_user,
            'username': username,
            'birth': birth,
            'sex': sex,
        }
        await self.update_user_info(user_info_dict)

    async def update_user_info(self, data_dict: dict) -> None:
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            await conn.execute(
                UserInfoTable.update().
                    where(UserInfoTable.c.U_ID == data_dict.get('U_ID')).
                    values(U_Name=data_dict.get('username'),
                           U_Sex=data_dict.get('sex'),
                           U_Birth=data_dict.get('birth'))
            )
            # aiomysql bug .commit()方法不存在
            # 这里直接调用实现即可 or conn.execute('commit')
            await conn._commit_impl()


default_handlers = [
    (r"/api/v1/userInfo/", UserInfoHandler),
]
