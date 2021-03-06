import time
from utils.redis import redis
from utils.AI import chat_conf as cf
from utils.request import request as req


class ChatRobot:
    """ 畅游的知U智能问答机器人 """
    def __init__(self):
        self.rs = redis.Redis()
        self.access_token = None
        self.time_stamp_now = int(time.time())
        self.deadline = 15  # access_token 过期时间 15天
        self.data = {
            'grant_type': cf.GRANT_TYPE,
            'client_id': cf.CLIENT_ID,
            'client_secret': cf.CLIENT_SECRET
        }

    def __access_token(self):
        result = req.post_api({
            'url': cf.API_URL['access_token'],
            'data': self.data,
        })
        time_stamp = int(time.time())
        self.rs.set_redis(name='zyou', mapping={'access_token': result['access_token'], 'time_stamp': time_stamp})
        return result['access_token']

    def inter_locution(self, ask):
        if not self.rs.exists('zyou'):
            self.access_token = self.__access_token()
        else:
            zyou = self.rs.get_redis(name='zyou', keys=['access_token', 'time_stamp'])
            sec = self.time_stamp_now - int(zyou[1])
            if sec > 3600 * 24 * self.deadline:
                self.access_token = self.__access_token()
            else:
                self.access_token = zyou[0]
        result = req.post_api({
            'url': cf.API_URL['interlocution'],
            'data': {
                'secretKey': cf.SECRET_KEY,
                'visitorId': 'abc123',
                'access_token': self.access_token,
                'question': ask,
            }
        })
        result['data']['text'] = result['data']['text'].replace('<p>', '').replace('</p>', '')
        return result['data']['text']


class QingYunKe:
    """ 青云客智能聊天机器人API url:http://api.qingyunke.com/ """
    def __init__(self):
        self.url = cf.QINGYUNKE_API

    def inter_locution(self, talk):
        result = req.get_api({
            'url': self.url,
            'data': {
                'key': 'free',
                'appid': 0,
                'msg': talk,
            }
        })
        result['content'] = result['content'].replace('br', '。').replace('菲菲', '小晗晗')
        return result['content']
