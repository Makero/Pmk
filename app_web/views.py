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
        openid = request.GET.get('openID')
        secret_key = request.GET.get('secretKey')
        rs = redis.Redis(db=1)
        secret = rs.get_redis(name='qrAuthUsers', key=openid)

        queryset = models.User.objects.all()
        s = serializers.UserSerializer(queryset, many=True)
        print(s.data)

        if secret == secret_key:
            auth_token = basics.create_token(openid)
            rs.set_redis(name='authToken:' + auth_token, mapping={'user': 'Maker', 'age': 27, 'sex': 0}, day=5)
            return Response({'code': '20001', 'authToken': auth_token}, status=status.HTTP_201_CREATED)

        return Response({'code': '40001', 'msg': '登录失败'}, status=status.HTTP_400_BAD_REQUEST)


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
