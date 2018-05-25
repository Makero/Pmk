import json
from django.http import HttpResponse
from utils.api import wechat
from utils.redis import redis


def index(req):
    result = {'code': 404, 'data': {}}

    if req.method == 'GET' and req.GET:
        check = wechat.Validate()
        val = check.check_signature(req.GET)
        result['code'] = 200
        result['method'] = 'get'
        result['data']['bool'] = val

    if req.method == 'POST' and req.POST:
        result['code'] = 200
        result['method'] = 'post'

    return HttpResponse(json.dumps(result))

def access(req):
    rs = redis.Redis()
    result = rs.get_redis(name="wechat", key="access_token")
    return HttpResponse(result)

def page_not_found(req):

    data = {'code': 404, 'data': {}}
    return HttpResponse(json.dumps(data))
