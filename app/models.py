from django.db import models

class Authorizer(models.Model):
    name = models.CharField(max_length=128, unique=True)
    cert = models.TextField(max_length=1024)

    def __unicode__(self):
        return self.name

class Resource(models.Model):
    # Max length based on QR code study
    name = models.CharField(max_length=213, unique=True)
    quantity = models.IntegerField(default=2147483648)
    authorizers = models.ManyToManyField(Authorizer)

    def __unicode__(self):
        return self.name


class LogRecord(models.Model):
    who = models.ForeignKey(Authorizer)
    when = models.DateTimeField(auto_now=True)
    what = models.CharField(max_length=213)

    def __unicode__(self):
        return '%s->%s' % (self.who, self.what)