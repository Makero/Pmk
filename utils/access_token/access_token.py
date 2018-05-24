import time
from threading import Thread
from utils.redis import redis
from wechat.api import wechat


class TimedRefresh:

    def __timed_refresh(self, sec, ss):

        __sec = sec

        while True:
            result = wechat.AccessToken().get()
            try:
                errcode = result['errcode']
            except KeyError:
                errcode = False

            if errcode:
                if errcode == -1:
                    sec = ss
                    print("\033[1;33m 系统繁忙，%ds后再次发起请求\033[0m" % (sec, ))
                else:
                    print("\033[1;31m ======\n", "刷新 access_token 出错\n", result, "\n======\033[0m")
                    return
            else:
                sec = __sec
                rs = redis.Redis()
                rs.set_redis(name='wechat', key='access_token', value=result['access_token'])
                print("\033[1;32m 刷新获取的 access_token 写入缓存成功\033[0m")

            time.sleep(sec)

    def start(self):

        Thread(target=self.__timed_refresh, args=(5400, 10, )).start()
        print("\033[1;32m 定时刷新 access_token 程序启动 成功\033[0m")
