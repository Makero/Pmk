import json
import time
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.http import HttpResponse
from app_wechat.utils.api import wechat, wechat_conf as wc
from app_wechat.utils.msg import handle
from utils.AI import chat
from utils.redis import redis
from app_wechat.utils.auth import auth
from app_web import models, serializers


def validate_token(req):
    """ 微信公众号调用平台时的token验证 """
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


class UserAuthView(APIView):
    """ 用户身份认证 """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        ak = auth.AuthKey()
        voucher = ak.is_auth_success(request.data.get('authKey'))

        if voucher:
            # 认证authKey成功
            openid_filter = models.User.objects.filter(openid=voucher.get('openID'))

            if openid_filter:
                print(openid_filter)
                username_filter = openid_filter.filter(username=request.data.get('userName'))
                if username_filter:
                    username_filter.update(sex=request.data.get('sex'))
                    ak.del_auth_msg(voucher.get('openID'), request.data.get('authKey'))
                    return Response({'code': '20001', 'data': voucher}, status=status.HTTP_201_CREATED)
                return Response({'code': '40002', 'msg': '昵称不正确'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                s = serializers.UserSerializer(data={'username': request.data.get('userName'),
                                                     'sex': request.data.get('sex'),
                                                     'openid': voucher.get('openID')})
                if s.is_valid():
                    s.save()
                    ak.del_auth_msg(voucher.get('openID'), request.data.get('authKey'))
                    return Response({'code': '20001', 'data': voucher}, status=status.HTTP_201_CREATED)
        return Response({'code': '40001', 'msg': '认证失败'}, status=status.HTTP_400_BAD_REQUEST)


def msg_handle(req):
    """ 公众号消息处理 """
    if req.method == 'POST':
        data = handle.MsgHandle(req.GET).start()
    else:
        data = {
            'code': 40001,
            'errmsg': "不能使用get请求访问"
        }

    return HttpResponse(json.dumps(data))


def msg_talk(req):
    """ 使用 知u 聊天机器人接口 """
    if req.method == 'POST':
        robot = chat.ChatRobot()
        data = robot.inter_locution(req.GET['talk'])
    else:
        data = {
            'code': 40001,
            'errmsg': "不能使用get请求访问"
        }

    return HttpResponse(json.dumps(data))


def qing_yun_ke(req):
    """ 使用 青云客 聊天机器人接口 """
    robot = chat.QingYunKe()
    data = robot.inter_locution(req.GET['talk'])

    return HttpResponse(json.dumps(data))


def wx_config(req):
    """ 微信jssdk 权限验证配置 """
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


def music(req):
    """ 音乐信息查询 """
    result = {'code': 404, 'data': {}}
    if req.method == 'GET' and req.GET:
        result['code'] = 200
        result['data'] = handle.Search().music_play(req.GET.get('songid'))
    return HttpResponse(json.dumps(result))


def music_lrc(req):
    """ 音乐歌词查询 """
    result = {'code': 404, 'data': {}}
    if req.method == 'GET' and req.GET:
        result['code'] = 200
        result['data'] = handle.Search().music_lrc(req.GET.get('songid'))
    return HttpResponse(json.dumps(result))
