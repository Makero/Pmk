import redis
from mk.db_conf import DB, ENV


class Redis:

    def __init__(self):

        db_conf = DB[ENV]['redis']

        self.host = db_conf['host']
        self.password = db_conf['password']
        self.port = db_conf['port']
        self.db = db_conf['db']
        self.rs = self.connect_redis()

    def connect_redis(self):
        return redis.StrictRedis(host=self.host, password=self.password, port=self.port, db=self.db)

    def get_redis(self, name, key):
        return self.rs.hget(name, key)

    def set_redis(self, name, key, value):
        return self.rs.hset(name, key, value)
