DEBUG = False  # 若需测试，建议不要在这里修改，见test文件夹下单元测试实现

# 密码加盐
PWD_SAULT = "this is not a password sault"
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
