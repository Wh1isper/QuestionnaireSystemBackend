from tornado.web import RequestHandler
from aioengine import get_engine
import json
import aiomysql
from typing import Any
import functools
from typing import Text
import re
from config import PASSWORD_REG



class BaseHandler(RequestHandler):
    def initialize(self):
        self.log_hook = None
        self.MISSING_DATA = 100
        self.engine = None

    def get_current_user(self) -> Any:
        return self.get_secure_cookie('user')

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
        return bool(re.search(PASSWORD_REG, pwd))


def authenticated(method):
    # 参考tornado.web.authenticated
    @functools.wraps(method)
    async def wrapper(self: BaseHandler, *args, **kwargs):
        if not self.current_user:
            return self.raise_HTTP_error(401)
        return await method(self, *args, **kwargs)

    return wrapper
