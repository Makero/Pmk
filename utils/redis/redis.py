import redis
from mk.db_conf import DB, ENV


class Redis:

    def __init__(self, db=None):

        db_conf = DB[ENV]['redis']

        self.host = db_conf['host']
        self.password = db_conf['password']
        self.port = db_conf['port']
        self.db = db or db_conf['db']
        self.rs = self.connect_redis()

    def connect_redis(self):
        return redis.StrictRedis(host=self.host, password=self.password, port=self.port, db=self.db)

    def exists(self, name):
        return self.rs.exists(name)

    def get_redis(self, name=None, key=None, keys=None):
        if keys is None:
            return self.rs.hget(name, key)
        else:
            return self.rs.hmget(name, keys)

    def set_redis(self, name=None, key=None, value=None, mapping=None):
        if mapping is None:
            return self.rs.hset(name, key, value)
        else:
            return self.rs.hmset(name, mapping)

    def del_redis(self, name=None, key=None):
        return self.rs.hdel(name, key)
