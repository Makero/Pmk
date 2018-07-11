from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from app_web import models

class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.query_params.get('token')
        token_obj = models.Token.objects.filter(token=token).first()
        if token_obj:
            return (token_obj.user, token_obj)
        raise exceptions.AuthenticationFailed("认证失败")

    # def authenticate_header(self, request):
    #     pass
