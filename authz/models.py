from django.db import models

class Authorizer(models.Model):
    name = models.CharField(max_length=128, unique=True)

class Resource(models.Model):
    name = models.CharField(max_length=256, unique=True)
    quantity = models.IntegerField(default=2147483648)
    authorizers = models.ManyToManyField(Authorizer)
