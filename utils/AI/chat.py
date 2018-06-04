from utils.redis import redis
from utils.AI import chat_conf as cf
from utils.request import request as req

class ChatRobot:
    def __init__(self):
        self.rs = redis.Redis()
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

        self.rs.set_redis(name='zyou', key='access_token', value=result['access_token'])

    def inter_locution(self, ask):
        access_token = self.rs.get_redis(name='zyou', key='access_token').decode('utf-8')
        result = req.post_api({
            'url': cf.API_URL['interlocution'],
            'data': {
                'secretKey': cf.SECRET_KEY,
                'visitorId': 'abc123',
                'access_token': access_token,
                'question': ask,
            }
        })
        result['data']['text'] = result['data']['text'].replace('<p>', '').replace('</p>', '')
        return result
