from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from utils.redis import redis


class UserTokenAuthentication(BaseAuthentication):

    def authenticate(self, request):
        try:
            name = "authToken:"+request.data['token']
        except KeyError:
            raise exceptions.AuthenticationFailed("认证失败")

        rs = redis.Redis(db=1)
        token_obj = rs.get_redis(name=name)

        if token_obj:
            return token_obj['user'], token_obj
        raise exceptions.AuthenticationFailed("认证失败")

    # def authenticate_header(self, request):
    #     pass
