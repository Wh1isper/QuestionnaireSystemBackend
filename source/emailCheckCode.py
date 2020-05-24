# 邮箱验证码生成
import random
from typing import List, Text
import aiosmtplib
from email.mime.text import MIMEText
from email.header import Header
from config import *


async def send_email_checkcode(email: Text) -> Text or None:
    def get_chars(chars: List = init_chars_E, length: int = email_checkcode_length) -> List:
        '''生成给定长度的字符串，返回列表格式'''
        return random.sample(chars, length)

    check_code = ''.join(c for c in get_chars())
    mail_msg = """
    <p>欢迎注册问卷调查系统</p>
    <p>您的验证码如下：{}</p>
    <p>邮件自动发送 请勿回复</p>
    """.format(check_code)
    message = MIMEText(mail_msg, 'html', 'utf-8')
    message['From'] = Header(EMAIL_ACCOUNT)
    # 163邮箱不支持utf-8的收件人
    message['To'] = Header(email)
    message['Subject'] = "问卷调查系统验证码"
    try:
        async with aiosmtplib.SMTP(SMTP_SERVERSE, SERVERS_PORT) as server:
            await server.login(EMAIL_ACCOUNT, AUTH_CODE)
            await server.sendmail(EMAIL_ACCOUNT, email, message.as_string())
    except aiosmtplib.SMTPException:
        return None
    return check_code


if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_email_checkcode('9573586@qq.com'))
