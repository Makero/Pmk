import json
from django.http import HttpResponse
from wechat.api import wechat


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

def page_not_found(req):

    data = {'code': 404, 'data': {}}
    return HttpResponse(json.dumps(data))
