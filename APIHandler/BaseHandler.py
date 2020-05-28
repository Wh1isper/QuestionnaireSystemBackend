from tornado.web import RequestHandler
from aioengine import get_engine
import json
import aiomysql
from typing import Any
import functools
from typing import Text
import re
from config import PASSWORD_REG
from orm import *


def authenticated(method):
    # 参考tornado.web.authenticated
    @functools.wraps(method)
    async def wrapper(self: RequestHandler, *args, **kwargs):
        if not self.current_user:
            return self.raise_HTTP_error(401)
        return await method(self, *args, **kwargs)

    return wrapper


class BaseHandler(RequestHandler):
    def initialize(self):
        self.log_hook = None
        self.MISSING_DATA = 100
        self.engine = None

    def get_current_user(self) -> Any:
        return int(self.get_secure_cookie('user'))

    def get_json_data(self) -> dict or None:
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return None
        return json_data

    def get_str_from_secure_cookie(self, name: Text):
        cookie_vaule = self.get_secure_cookie(name)
        return str(cookie_vaule, encoding='utf-8') if cookie_vaule else None

    def set_default_headers(self) -> None:
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')

    def raise_HTTP_error(self, state_code: int, *msg_code: int or None) -> None:
        if msg_code:
            msg = {'msg': msg_code}
            self.write(msg)
        self.set_status(state_code)

    async def get_engine(self) -> aiomysql.sa.engine.Engine:
        if not self.engine:
            self.engine = await get_engine()
        return self.engine

    def log(self) -> None:

        log_dict = {
            'ip': self.request.remote_ip,
            'state': self.get_status(),
            'method': self.request.method,
            'Handler': self.__class__.__name__,
            'cookie': self.request.headers.get('Cookie'),
            'body': str(self.request.body, encoding='utf-8'),
        }
        print(json.dumps(log_dict))

    def on_finish(self) -> None:
        if self.log_hook:
            self.log_hook()
        else:
            self.log()

    def valid_pwd_reg(self, pwd: Text) -> bool:
        # 验证密码强度
        return bool(re.search(PASSWORD_REG, pwd))

    @authenticated
    async def valid_user_questionnaire_relation(self, q_id: int) -> bool:
        # 鉴别用户是否是问卷的拥有者
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.U_ID == self.current_user)
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id))
            questionnaire_info = await result.fetchone()
        return bool(questionnaire_info)

    @authenticated
    async def get_questionnaire_state(self, q_id: int) -> int:
        # 返回问卷状态
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.U_ID == self.current_user)
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id))
            questionnaire_info = await result.fetchone()
        return questionnaire_info.QI_State
