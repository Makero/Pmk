###########################
#
# 微信API调用的方法
#
###########################
import hashlib
from urllib import parse
from utils.api import wechat_conf as wx
from utils.request import request as req


class Validate:
    """验证类"""
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
    """获取access_token类"""
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
        return result


class Ticket:
    def __init__(self, token):
        self.url = wx.API_URL['jsapi_ticket']
        self.data = {
            'type': 'jsapi',
            'access_token': token,
        }

    def get_signature(self, param):
        """获取token加密签名"""
        dicts = sorted(param.items(), key=lambda d: d[0])
        tmp = parse.urlencode(dicts)
        _str = parse.unquote(tmp).encode(encoding='UTF-8')
        return hashlib.sha1(_str).hexdigest()

    def get(self):
        result = req.get_api({
            'url': self.url,
            'data': self.data,
        })
        return result.get("ticket")
