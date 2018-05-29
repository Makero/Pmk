from django.db import models

# Create your models here.
class Auth(models.Model):
    openid = models.CharField(max_length=30)
    date = models.CharField(max_length=30)

class Person(models.Model):
    name = models.CharField(max_length=30)
    talk = models.CharField(max_length=60)