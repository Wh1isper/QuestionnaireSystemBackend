from tornado.web import RequestHandler
from aioengine import get_engine
import json
import aiomysql


class BaseHandler(RequestHandler):
    def initialize(self):
        self.log_hook = None
        self.MISSING_DATA = 100
        self.engine = None

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')

    def raise_HTTP_error(self, state_code: int, msg_code: int) -> None:
        msg = {'msg': msg_code}
        self.set_status(state_code)
        self.write(msg)

    async def get_engine(self) -> aiomysql.sa.engine.Engine:
        if not self.engine:
            self.engine = await get_engine()
        return self.engine

    def log(self) -> None:
        log_dict = {
            'ip': self.request.remote_ip,
            'method': self.request.method,
            'headers': self.request.headers,
            'body': self.request.body,
        }
        print(json.dumps(log_dict))

    def on_finish(self) -> None:
        if self.log_hook:
            self.log_hook()
        else:
            self.log()
