import json
import hashlib
from django.http import HttpResponse


class ValidateToken:

    def __init__(self):
        self.token = 'lkyn20180403'
        self.signature = None
        self.bool = False

    def get_signature(self, timestamp, nonce):
        """获取token加密签名"""
        tmp = [self.token, timestamp, nonce]
        tmp.sort()
        str = ''.join(tmp).encode(encoding='UTF-8')
        self.signature = hashlib.sha1(str).hexdigest()

    def check_signature(self, param):
        """检测token加密签名是否正确"""
        self.get_signature(param.get('timestamp'), param.get('nonce'))

        if self.signature == param.get('signature'):
            self.bool = True

        return self.bool


def index(req):
    result = {'code': 404, 'data': {}}

    if req.method == 'GET':
        check = ValidateToken()
        val = check.check_signature(req.GET)
        result['code'] = 200
        result['method'] = 'get'
        result['data']['bool'] = val

    if req.method == 'POST':
        result['code'] = 200
        result['method'] = 'post'

    return HttpResponse(json.dumps(result))


def page_not_found():

    data = {'code': 404, 'data': {}}
    return HttpResponse(json.dumps(data))
