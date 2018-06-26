##############################################
#
# 启动一个进程无限循环定时刷新access_token
# access_token存储到redis缓存中
# 刷新时间为 5400s,如果异常将退出循环
# 如果系统繁忙，将每10s再次发起请求
#
##############################################
import time
from threading import Thread
from utils.api import wechat
from utils.redis import redis


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
                ticket = wechat.Ticket(result['access_token'])
                params = {'noncestr': 'Wm3WZYTPz2xwyzaW', 'jsapi_ticket': ticket.get(), 'timestamp': int(time.time()), 'url': "http://www.20mk.cn/wechat/talk", }

                signature = ticket.get_signature(params)
                params.update({'access_token': result['access_token'], 'signature': signature})
                rs.set_redis(name='wechat', mapping=params)
                print("\033[1;32m 刷新获取的 access_token 写入缓存 成功\033[0m")

            time.sleep(sec)

    def start(self):

        Thread(target=self.__timed_refresh, args=(5400, 10, )).start()
        print("\033[1;32m 定时刷新 access_token 程序启动 成功\033[0m")
