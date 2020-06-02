from BaseHandler import BaseHandler, authenticated,xsrf
from typing import Any


class AdminBaseHandler(BaseHandler):
    def get_current_user(self) -> Any:
        return self.get_secure_cookie('admin')

