from django.db import models


class Subscribe(models.Model):
    openid = models.CharField(max_length=30)
    create_date = models.DateField()
    cancel_date = models.DateField()
    status = models.CharField(max_length=10)
