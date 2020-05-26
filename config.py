DEBUG = True  # 需要http请求测试时开启，单元测试时请在单元测试内设置
ADMIN_ACOUNT = 'admin'
ADMIN_PASSWORD = 'c214ab5d94c0a6655a8e890af8e4bb28966c96d7b627c01db2033d5ad255355c'  # password12345 由encrypt.password_encrypt生成
# 密码加盐
PWD_SALT = "this is not a password salt"
# cookie加盐
COOKIE_SECRET = "this is not a secret cookie"
# 验证码配置 check_code_config
_letter_cases = "abcdefghjkmnpqrstuvwxy"  # 小写字母，去除可能干扰的i，l，o，z
_upper_cases = _letter_cases.upper()  # 大写字母
_numbers = ''.join(map(str, range(3, 10)))  # 数字
# 最终生成的候选字母表
init_chars = ''.join((_letter_cases, _upper_cases, _numbers))
# 邮箱验证码配置 email_checkcode_config
_letter_cases_E = "abcdefghijklmnopqrstuvwxyz"
_upper_cases_E = _letter_cases_E.upper()
_numbers_E = ''.join(map(str, range(1, 10)))
# 最终生成的候选字母
init_chars_E = ''.join((_letter_cases_E, _upper_cases_E, _numbers_E))
email_checkcode_length = 6
# 邮箱配置
EMAIL_ACCOUNT = 'qs_test@163.com'
AUTH_CODE = 'HCNWVDYOBDPTBYHN'
SMTP_SERVERSE = 'smtp.163.com'
SERVERS_PORT = 25
# 密码强度正则
PASSWORD_REG = r'^[A-Za-z0-9]+$'
