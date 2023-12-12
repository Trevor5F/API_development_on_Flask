import base64
import hashlib
import hmac

from dao.user import UserDAO
from helpers.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    # для аутентификации
    def get_user_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def get_one(self, mid):
        return self.dao.get_one(mid)

    def get_all(self):
        return self.dao.get_all()

    def create(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.create(user_d)

    def update(self, user_d):
        user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.update(user_d)

    def partial_update(self, user_d):
        if user_d["password"]:
            user_d["password"] = self.get_hash(user_d["password"])
        return self.dao.partial_update(user_d)

    def delete(self, rid):
        self.dao.delete(rid)


    def get_hash(self, password): # хеширование пароля
        return base64.b64encode(
            hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        ))

    def compare_passwords(self, password_hash, other_password) -> bool: # сравнение паролей
        # print(password_hash)
        decoded_digest = base64.b64decode(password_hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            other_password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decoded_digest, hash_digest)
