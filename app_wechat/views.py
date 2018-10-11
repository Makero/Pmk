import time
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app_wechat.utils.api import wechat, wechat_conf as wc
from app_wechat.utils.msg import handle
from app_wechat.utils.auth import auth
from utils.AI import chat
from utils.redis import redis
from app_web import models, serializers
from urllib import request as req
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class ValidateTokenView(APIView):
    """ 微信公众号调用平台时的token验证 """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        check = wechat.Validate()
        val = check.check_signature(request.data)
        return Response({'code': '20001', 'data': {'bool': val}}, status=status.HTTP_201_CREATED)


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


class MsgHandleView(APIView):
    """ 公众号消息处理 """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        print(request.data)
        data = handle.MsgHandle(request.data).start()
        return Response({'code': '20001', 'data': data}, status=status.HTTP_201_CREATED)


class ZyouRobotView(APIView):
    """ 使用 知u 聊天机器人接口 """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        robot = chat.ChatRobot()
        result = robot.inter_locution(request.data['talk'])
        return Response({'code': '20001', 'data': {'content': result}}, status=status.HTTP_201_CREATED)


class QYKView(APIView):
    """ 使用 青云客 聊天机器人接口 """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        robot = chat.QingYunKe()
        result = robot.inter_locution(request.data['talk'])
        return Response({'code': '20001', 'data': {'content': result}}, status=status.HTTP_201_CREATED)


class WxConfigView(APIView):
    """ 微信jssdk 权限验证配置 """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        rs = redis.Redis()
        signame = request.data['signame']
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
            return Response({'code': '20001', 'data': data}, status=status.HTTP_201_CREATED)
        return Response({'code': '40001', 'msg': 'redis的wechat表不存在，定时刷新access_token功能没有开启'},
                        status=status.HTTP_400_BAD_REQUEST)


class MusicView(APIView):
    """ 音乐信息查询 """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        result = handle.Search().music_play(request.data['songid'])
        return Response({'code': '20001', 'data': result}, status=status.HTTP_201_CREATED)


class MusicLRCView(APIView):
    """ 音乐歌词查询 """
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        result = handle.Search().music_lrc(request.data.get('songid'))
        return Response({'code': '20001', 'data': result}, status=status.HTTP_201_CREATED)


class SaveImage(APIView):
    """保存图片"""
    permission_classes = ()
    authentication_classes = ()

    def get(self, request):
        rs = redis.Redis()
        access_token = rs.get_redis(name='wechat', key='access_token')
        serverId = request.data.get('serverId')
        img_link = wc.API_URL['save_image'] + "?access_token=" + access_token + "&media_id=" + serverId
        path = "/home/mkfile/upload/" + serverId + ".jpg"
        req.urlretrieve(img_link, path)
        return Response({'code': '20001', 'data': {'url': 'http://www.20mk.cn/mkfile/upload/' + serverId + ".jpg"}}, status=status.HTTP_201_CREATED)
