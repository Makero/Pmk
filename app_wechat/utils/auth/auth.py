##############################
#
# 微信公众号用户认证
# 目的：获取用户openID
#
# 2018/07/06
##############################
from utils.redis import redis
from utils import basics
import hashlib


class AuthKey:

    def __init__(self, openid=None):
        self.openID = openid
        self.authKey = None
        self.redis = redis.Redis(db=1)
        self.usersTable = 'authUsers'
        self.keysTable = 'authKeys'

    def query_authkey(self):
        """ 查询authkey """
        self.authKey = self.redis.get_redis(name=self.usersTable, key=self.openID)

    def create_authkey(self):
        """ 创建authkey """
        _nonce_str = basics.create_random_string(16)
        _st = _nonce_str + self.openID
        self.authKey = hashlib.md5(_st.encode(encoding='utf-8')).hexdigest()
        self.redis.set_redis(name=self.usersTable, key=self.openID, value=self.authKey)
        self.redis.set_redis(name=self.keysTable, key=self.authKey, value=self.openID)

    def query_or_create(self):
        """ 查询或创建authkey """
        if not self.redis.exists(self.usersTable):
            self.create_authkey()
        else:
            self.query_authkey()
            if not self.authKey:
                self.create_authkey()

        if type(self.authKey) is bytes:
            self.authKey = str(self.authKey, encoding='utf-8')

        return self.authKey

    def is_auth_success(self, authkey):
        """ 判断认证是否成功  认证成功返回 openid 值   认证失败返回 False """
        openid = self.redis.get_redis(name=self.keysTable, key=authkey)
        if openid:
            self.redis.del_redis(name=self.keysTable, key=authkey)
            self.redis.del_redis(name=self.usersTable, key=openid)
        if type(openid) is bytes:
            openid = str(openid, encoding='utf-8')
        return openid or False

