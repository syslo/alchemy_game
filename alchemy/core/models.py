from django.db import models
from django.conf import settings


class Item(models.Model):
    name = models.CharField(max_length=32, unique=True)
    limit = models.PositiveIntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class Rule(models.Model):
    input1 = models.ForeignKey(Item, related_name='+')
    input2 = models.ForeignKey(Item, related_name='+')
    result = models.ForeignKey(Item, related_name='+')

    class Meta:
        unique_together = (('input1', 'input2'),)

    def __str__(self):
        return '%s + %s -> %s' % (self.input1, self.input2, self.result)


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='accounts')
    item = models.ForeignKey(Item, related_name='accounts')
    credit = models.PositiveIntegerField()

    class Meta:
        unique_together = (('user', 'item'),)

    def __str__(self):
        return '%s has %d of %s' % (self.user, self.credit, self.item)


class LogItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logs')
    type = models.CharField(max_length=16)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '[%s]: %s' % (self.datetime, self.text)
