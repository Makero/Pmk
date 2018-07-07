from django.db import models


class User(models.Model):
    SEX_TYPE = (
        ('0', '男'),
        ('1', '女')
    )
    name = models.CharField('账号', max_length=32, unique=True)
    password = models.CharField('密码', max_length=32)
    openid = models.CharField('微信用户唯一标识', max_length=30)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = verbose_name

    def is_authenticated(self):
        pass

    def __str__(self):
        return self.name


class Token(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=32)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user
