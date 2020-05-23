from BaseHandler import BaseHandler
from source import emailCheckCode, checkCode
import io
import time
import json


class CheckcodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        # 返回验证码 set-cookie:check_code为验证码
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E7%99%BB%E5%BD%95%E9%AA%8C%E8%AF%81%E7%A0%81api
        imgio = io.BytesIO()
        img, code = checkCode.create_validate_code()
        img.save(imgio, 'GIF')
        self.set_header("Content-Type", "image/gif")
        self.write(imgio.getvalue())
        # 10分钟过期的cookie
        self.set_secure_cookie("check_code", code, expires_days=None, expires=time.time() + 60 * 10)


class EmailCheckcodeHandler(BaseHandler):
    def initialize(self):
        BaseHandler.initialize(self)
        self.SEND_CHECK_CODE_FAIL = 1

    async def post(self, *args, **kwargs):
        # 向邮箱发送验证码，set-cookie:email_check_code为验证码内容
        # 接口约定：https://github.com/Wh1isper/QuestionnaireSystemDoc/blob/master/%E6%8E%A5%E5%8F%A3%E5%AE%9A%E4%B9%89/%E6%8E%A5%E5%8F%A3%E8%AE%BE%E8%AE%A1-2020.05.17-V1.0.md#%E9%82%AE%E7%AE%B1%E9%AA%8C%E8%AF%81%E7%A0%81api
        try:
            json_data: dict = json.loads(self.request.body.decode('utf-8'))
        except json.decoder.JSONDecodeError:
            return self.raise_HTTP_error(401, self.MISSING_DATA)
        email = json_data.get('email')
        if not email:
            return self.raise_HTTP_error(401, self.MISSING_DATA)
        email_check_code = await emailCheckCode.send_email_checkcode(email)
        if not email_check_code:
            return self.raise_HTTP_error(401, self.SEND_CHECK_CODE_FAIL)
        self.set_secure_cookie('email_check_code', email_check_code)
        self.set_status(200)


default_handlers = [
    (r"/api/v1/checkCode/", CheckcodeHandler),
    (r"/api/v1/emailCode/", EmailCheckcodeHandler),
]
