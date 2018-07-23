from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from utils.redis import redis


class UserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            name = "authToken:"+request.META.get('HTTP_TOKEN')
        except KeyError:
            raise exceptions.AuthenticationFailed("认证失败")

        rs = redis.Redis(db=1)
        token_obj = rs.get_redis(name=name)

        if token_obj:
            return token_obj['user'], request.META.get('HTTP_TOKEN')
        raise exceptions.AuthenticationFailed("认证失败")

    # def authenticate_header(self, request):
    #     pass
