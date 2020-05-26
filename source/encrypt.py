import hashlib
from typing import Text

def password_encrypt(pwd:Text, sault:Text):
    encrypt_password = hashlib.sha256(pwd.encode('utf-8'))
    encrypt_password.update(sault.encode('utf-8'))
    return encrypt_password.hexdigest()


if __name__ == '__main__':
    from config import PWD_SAULT
    secure_pwd = password_encrypt('password12345',PWD_SAULT)
    print(secure_pwd)