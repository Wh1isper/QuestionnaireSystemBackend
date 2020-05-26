from BaseHandler import BaseHandler, authenticated
from typing import Text
import json
import datetime
from config import DEBUG


class LoginHandler(BaseHandler):
    @authenticated
    async def post(self, *args, **kwargs):
        # 获取当前用户问卷列表
        pass
