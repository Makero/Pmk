from django.db import models


class Subscriber(models.Model):
    STATUS_TYPE = (
        ('S', 'Subscribe'),
        ('U', 'Unsubscribe')
    )
    openid = models.CharField(max_length=30)
    status = models.CharField(max_length=1, choices=STATUS_TYPE)

    class Meta:
        app_label = "wechat"


class Operation(models.Model):
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    date = models.DateTimeField(null=True)
    status = models.CharField(max_length=1, choices=Subscriber.STATUS_TYPE)

    class Meta:
        app_label = "wechat"
