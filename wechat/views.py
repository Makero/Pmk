import json
from django.http import HttpResponse
from utils.api import wechat
from utils.msg import handle


def validate_token(req):
    result = {'code': 404, 'data': {}}

    if req.method == 'GET' and req.GET:
        check = wechat.Validate()
        val = check.check_signature(req.GET)
        result['code'] = 200
        result['method'] = 'get'
        result['data']['bool'] = val

    if req.method == 'POST' and req.GET:
        result['code'] = 200
        result['method'] = 'post'

    return HttpResponse(json.dumps(result))


def msg_handle(req):
    if req.method == 'POST':
        data = handle.MsgHandle(req.GET).start()
    else:
        data = {
            'code': 40001,
            'errmsg': "不能使用get请求访问"
        }

    return HttpResponse(json.dumps(data))


def page_not_found(req):

    data = {'code': 404, 'data': {}}
    return HttpResponse(json.dumps(data))


def music(req):
    result = {'code': 404, 'data': {}}
    if req.method == 'GET' and req.GET:
        result['code'] = 200
        result['data'] = handle.Search().music_play(req.GET.get('songid'))
    return HttpResponse(json.dumps(result))


def music_lrc(req):
    result = {'code': 404, 'data': {}}
    if req.method == 'GET' and req.GET:
        result['code'] = 200
        result['data'] = handle.Search().music_lrc(req.GET.get('songid'))
    return HttpResponse(json.dumps(result))
