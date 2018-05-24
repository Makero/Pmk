import hashlib
from utils.request import request as req
from wechat.api import wechat_api_conf as wx


class Validate:

    def __init__(self):
        self.token = wx.TOKEN
        self.signature = None
        self.bool = False

    def get_signature(self, timestamp, nonce):
        """获取token加密签名"""
        tmp = [self.token, timestamp, nonce]
        tmp.sort()
        _str = ''.join(tmp).encode(encoding='UTF-8')
        self.signature = hashlib.sha1(_str).hexdigest()

    def check_signature(self, param):
        """检测token加密签名是否正确"""
        self.get_signature(param.get('timestamp'), param.get('nonce'))

        if self.signature == param.get('signature'):
            self.bool = True

        return self.bool


class AccessToken:

    def __init__(self):
        self.url = wx.API_URL['access_token']
        self.data = {
            'grant_type': 'client_credential',
            'appid': wx.APP_ID,
            'secret': wx.APP_SECRET,
        }

    def get(self):
        """获取access_token"""
        result = req.get_api({
            'url': self.url,
            'data': self.data,
        })
        # if result['access_token']:
        #     rs = redis.Redis()
        #     rs.set_redis(name='wechat', key='access_token', value=result['access_token'])
        #     data = {"code": 200, "msg": "success"}
        # else:
        #     data = {"code": result['errcode'], "msg": result['errmsg']}

        return result
