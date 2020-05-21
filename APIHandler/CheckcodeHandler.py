from BaseHandler import BaseHandler
import io
from source import checkCode


class CheckcodeHandler(BaseHandler):
    def get(self, *args, **kwargs):
        imgio = io.BytesIO()
        img, code = checkCode.create_validate_code()
        img.save(imgio, 'GIF')
        self.set_header("Content-Type", "image/gif")
        self.write(imgio.getvalue())
        import time
        # 10分钟过期的cookie
        self.set_secure_cookie("check_code", code, expires_days=None, expires=time.time()+60*10)
