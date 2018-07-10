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
        return redis.StrictRedis(host=self.host, password=self.password,
                                 port=self.port, db=self.db, decode_responses=True)

    def exists(self, name):
        return self.rs.exists(name)

    def get_redis(self, name=None, key=None, keys=None):
        if keys is not None:
            return self.rs.hmget(name, keys)
        elif key is not None:
            return self.rs.hget(name, key)
        else:
            return self.rs.hgetall(name)

    def set_redis(self, name=None, key=None, value=None, mapping=None, day=None, sec=None):
        if mapping is not None:
            result = self.rs.hmset(name, mapping)
        else:
            result = self.rs.hset(name, key, value)
        if day is not None:
            self.over_time(name=name, day=day)
        elif sec is not None:
            self.over_time(name=name, sec=sec)
        return result

    def del_redis(self, name=None, key=None):
        if key is not None:
            result = self.rs.hdel(name, key)
        else:
            result = self.rs.delete(name)
        return result

    def over_time(self, name=None, day=None, sec=None):
        if sec is not None:
            time = sec
        else:
            time = day * 24 * 3600
        return self.rs.expire(name, time)
