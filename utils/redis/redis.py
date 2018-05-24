import redis
from utils.redis import redis_conf as rc


class Redis:

    def __init__(self):
        self.host = rc.params[rc.flag]['host']
        self.password = rc.params[rc.flag]['password']
        self.port = rc.params[rc.flag]['port']
        self.db = rc.params[rc.flag]['db']
        self.rs = self.connect_redis()

    def connect_redis(self):
        return redis.StrictRedis(host=self.host, password=self.password, port=self.port, db=self.db)

    def get_redis(self, name, key):
        return self.rs.hget(name, key)

    def set_redis(self, name, key, value):
        return self.rs.hset(name, key, value)
