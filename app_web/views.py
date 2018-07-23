from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils import basics
from utils.redis import redis
from app_web import models, serializers, filter


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


class CheckAuthTokenView(APIView):
    """ 验证authToken是否有效  """
    permission_classes = ()
    authentication_classes = ()

    def post(self, request):
        auth_token = request.data.get('authToken')
        rs = redis.Redis(db=1)
        user_data = rs.get_redis(name='authToken:'+auth_token)
        if len(user_data):
            return Response({'code': '20001', 'data': user_data}, status=status.HTTP_201_CREATED)
        return Response({'code': '40001', 'msg': 'authToken无效'}, status=status.HTTP_400_BAD_REQUEST)


class ArticleViewSet(viewsets.ModelViewSet):
    """ 文章 """
    permission_classes = ()
    authentication_classes = ()

    queryset = models.Article.objects.all().order_by('-create_time')
    serializer_class = serializers.ArticleSerializer
    filter_fields = ('author', 'type')
    search_fields = ('title', 'content', 'author')
    filter_class = filter.ArticleDateFilter


class MoodViewSet(viewsets.ModelViewSet):
    """ 心情 """
    queryset = models.Mood.objects.all().order_by('-create_time')
    serializer_class = serializers.MoodSerializer
    filter_fields = ('user_id',)
    filter_class = filter.MoodDateFilter


class CommentViewSet(viewsets.ModelViewSet):
    """ 评论 """
    queryset = models.Comment.objects.all().order_by('-comment_time')
    serializer_class = serializers.CommentSerializer
    filter_fields = ('topic_id',)


class ReplyViewSet(viewsets.ModelViewSet):
    """ 回复 """
    queryset = models.Reply.objects.all()
    serializer_class = serializers.ReplySerializer
    filter_fields = ('reply_id',)
