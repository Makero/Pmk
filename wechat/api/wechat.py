import hashlib
from wechat.api import wechat_api_conf as wx


class Validate:

    def __init__(self):
        self.token = wx.WX_TOKEN
        self.signature = wx.WX_SIGNATURE
        self.bool = wx.WX_BOOL

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
