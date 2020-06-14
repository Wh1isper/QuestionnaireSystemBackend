from tornado.web import RequestHandler
from aioengine import get_engine
import json
import aiomysql
from typing import Any
import functools
from typing import Text
import re
from config import PASSWORD_REG, DEBUG, UNITTEST
from orm import *
import time


class BaseHandler(RequestHandler):
    def initialize(self):
        self.log_hook = None
        self.MISSING_DATA = 100
        self.engine = None
        self.XSRF_NAME = '_xsrf'
        # 状态编码 枚举类太难用了
        self.USER_STATE_NORMAL = 0
        self.USER_STATE_BAN = 1
        self.Q_STATE_UNPUBLISH = 0
        self.Q_STATE_PUBLISHED = 1
        self.Q_STATE_INACTIVATE = 2
        self.Q_STATE_BAN = 3

    def get_current_user(self) -> Any:
        return int(self.get_secure_cookie('user'))

    def get_json_data(self) -> dict or None:
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return None
        return json_data

    def get_str_from_secure_cookie(self, name: Text):
        cookie_value = self.get_secure_cookie(name)
        return str(cookie_value, encoding='utf-8') if cookie_value else None

    def set_default_headers(self) -> None:
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def raise_HTTP_error(self, state_code: int, msg_code=None) -> None:
        self.set_status(state_code)
        self.send_error(state_code, msg=msg_code)

    def write_error(self, status_code: int, **kwargs: Any) -> None:
        self.write({
            'status': status_code,
            'msg': kwargs.get("msg")})
        self.finish()

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

    async def valid_user_questionnaire_relation(self, q_id: int) -> bool:
        # 鉴别用户是否是问卷的拥有者
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.U_ID == self.current_user)
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id))
            questionnaire_info = await result.fetchone()
        return bool(questionnaire_info)

    async def get_questionnaire_state(self, q_id: int) -> int:
        # 返回问卷状态,仅问卷拥有者可用
        engine = await self.get_engine()
        async with engine.acquire() as conn:
            result = await conn.execute(QuestionNaireInfoTable.select()
                                        .where(QuestionNaireInfoTable.c.U_ID == self.current_user)
                                        .where(QuestionNaireInfoTable.c.QI_ID == q_id))
            questionnaire_info = await result.fetchone()
        return questionnaire_info.QI_State

    def datetime_to_timestamp(self, date_time):
        if date_time:
            return time.mktime(date_time.timetuple())
        else:
            return None


def authenticated(method):
    # 参考tornado.web.authenticated
    @functools.wraps(method)
    async def wrapper(self: BaseHandler, *args, **kwargs):
        if not self.current_user:
            return self.raise_HTTP_error(401)
        return await method(self, *args, **kwargs)

    return wrapper


def xsrf(method):
    # xsrf验证
    @functools.wraps(method)
    async def wrapper(self: BaseHandler, *args, **kwargs):
        if not UNITTEST and not self.get_cookie(self.XSRF_NAME):
            return self.raise_HTTP_error(403)
        return await method(self, *args, **kwargs)

    return wrapper
