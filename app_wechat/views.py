import json
import time
from django.http import HttpResponse
from app_wechat.utils.api import wechat, wechat_conf as wc
from app_wechat.utils.msg import handle
from utils import basics
from utils.AI import chat
from utils.redis import redis
from app_wechat.utils.auth import auth


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


def user_auth(req):
    result = {'code': 404, 'data': {}}
    if req.method == 'POST':
        ak = auth.AuthKey()
        voucher = ak.is_auth_success(req.GET.get('authKey'))
        if voucher:
            result['data'] = voucher
            result['code'] = '200'

    return HttpResponse(json.dumps(result))


# 登录 身份校验生成authToken
def login_identity_check(req):
    result = {'code': 404, 'data': {}}
    if req.method == 'POST':
        openid = req.GET.get('openID')
        secret_key = req.GET.get('secretKey')
        rs = redis.Redis(db=1)
        secret = rs.get_redis(name='qrAuthUsers', key=openid)
        if type(secret) is bytes:
            secret = str(secret, encoding='utf-8')
        if secret == secret_key:
            auth_token = basics.create_token(openid)
            rs.set_redis(name='authToken', key=auth_token, value=openid)
            result['data']['authToken'] = auth_token
            result['code'] = 200

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

    result = {'code': 404, 'data': {'err': 'redis的wechat不存在'}}
    if req.method == 'POST':
        rs = redis.Redis()
        signame = req.GET.get('signame')
        conf = rs.get_redis(name='wechat', keys=['jsapi_ticket', 'access_token'])
        if conf[0] is not None:
            params = {'timestamp': int(time.time()),
                      'noncestr': wc.NONCESTR,
                      'jsapi_ticket': conf[0],
                      'url': wc.JSAPI_URLS[signame]
                      }
            ticket = wechat.Ticket(conf[1])
            data = {'appid': wc.APP_ID,
                    'timestamp': params['timestamp'],
                    'noncestr': params['noncestr'],
                    'signature': ticket.get_signature(params)
                    }
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
