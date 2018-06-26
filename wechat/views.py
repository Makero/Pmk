import json
from django.http import HttpResponse
from utils.api import wechat
from utils.api import wechat_conf as wc
from utils.msg import handle
from utils.AI import chat
from utils.redis import redis


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


# 使用 知u 聊天机器人接口 #
def msg_talk(req):
    if req.method == 'POST':
        robot = chat.ChatRobot()
        data = robot.inter_locution(req.GET['talk'])
    else:
        data = {
            'code': 40001,
            'errmsg': "不能使用get请求访问"
        }

    return HttpResponse(json.dumps(data))


# 使用 青云客 聊天机器人接口 #
def qing_yun_ke(req):

    robot = chat.QingYunKe()
    data = robot.inter_locution(req.GET['talk'])

    return HttpResponse(json.dumps(data))


def wx_config(req):
    result = {'code': 404, 'data': {'err':'redis的wechat不存在'}}
    if req.method == 'POST':
        rs = redis.Redis()
        conf = rs.get_redis(name='wechat', keys=['timestamp', 'noncestr', 'signature'])
        if conf[0] is not None:
            data = {'appid': wc.APP_ID, 'timestamp': conf[0].decode('utf-8'), 'noncestr': conf[1].decode('utf-8'), 'signature': conf[2].decode('utf-8')}
            result['code'] = 200
            result['data'] = data
    return HttpResponse(json.dumps(result))


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
