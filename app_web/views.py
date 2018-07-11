import json
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from utils import basics
from utils.redis import redis
from app_web import models, serializers


def login(req):
    """ 扫码登录 身份校验生成authToken """
    result = {'code': 404, 'data': {}}
    if req.method == 'POST':
        openid = req.GET.get('openID')
        secret_key = req.GET.get('secretKey')
        rs = redis.Redis(db=1)
        secret = rs.get_redis(name='qrAuthUsers', key=openid)

        if secret == secret_key:
            auth_token = basics.create_token(openid)
            rs.set_redis(name='authToken:'+auth_token, mapping={''}, day=5)
            result['data']['authToken'] = auth_token
            result['code'] = 200

    return HttpResponse(json.dumps(result))


class RegisterView(APIView):
    """ 用户注册 """
    authentication_classes = ()
    permission_classes = ()
    def post(self, request):
        s = serializers.UserSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
