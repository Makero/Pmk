from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import basics
from utils.redis import redis
from app_web import models, serializers


class LoginView(APIView):
    """ 扫码登录 身份校验生成authToken """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        openid = request.data.get('openID')
        secret_key = request.data.get('secretKey')
        if openid is None or secret_key is None:
            return Response({'code': '40001', 'msg': '没有身份认证'}, status=status.HTTP_400_BAD_REQUEST)

        rs = redis.Redis(db=1)
        secret = rs.get_redis(name='qrAuthUsers', key=openid)

        if secret == secret_key:
            data = models.User.objects.get(openid=openid)

            auth_token = basics.create_token(openid)
            rs.set_redis(name='authToken:' + auth_token, mapping={'id': data.id,
                                                                  'user': data.username,
                                                                  'sex': data.sex,
                                                                  'introduction': data.introduction,
                                                                  'head_path': data.head_path}, day=5)
            return Response({'code': '20001', 'data': {'authToken': auth_token}}, status=status.HTTP_201_CREATED)

        return Response({'code': '40001', 'msg': '登录失败'}, status=status.HTTP_400_BAD_REQUEST)
