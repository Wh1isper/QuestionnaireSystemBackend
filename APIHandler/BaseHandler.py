from tornado.web import RequestHandler


class BaseHandler(RequestHandler):
    def initialize(self):
        self.MISSING_DATA = 100

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Max-Age', 1000)
        # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Headers', '*')

    def raise_error(self, state_code: int, msg_code: int):
        msg = {'msg': msg_code}
        self.set_status(state_code)
        self.write(msg)

