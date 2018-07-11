from django.db import models
import django.utils.timezone as timezone


class Subscriber(models.Model):
    """ 公众号订阅 """
    STATUS_TYPE = (
        ('S', '订阅'),
        ('U', '退订')
    )
    openid = models.CharField('微信用户唯一标识', max_length=30)
    status = models.CharField('状态', max_length=1, choices=STATUS_TYPE)

    class Meta:
        app_label = "app_wechat"


class Operation(models.Model):
    """ 用户操作事件 """
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    date = models.DateTimeField('操作日期', default=timezone.now)
    status = models.CharField('状态', max_length=1, choices=Subscriber.STATUS_TYPE)

    class Meta:
        app_label = "app_wechat"
