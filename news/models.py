from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Channel(models.Model):
    name = models.TextField(verbose_name=_('Channel name'), max_length=50, unique=True)

    class Meta:
        verbose_name = 'Channel'
        verbose_name_plural = 'Channels'


class Segment(models.Model):
    channel = models.ForeignKey(Channel)
    start_ts = models.IntegerField(verbose_name=_('Start timestamp'))
    end_ts = models.IntegerField(verbose_name=_('End timestamp'))


class Topic(models.Model):
    name = models.TextField(verbose_name=_('Topic'), max_length=200)
    segment = models.ForeignKey(Segment)
    count = models.IntegerField()
    score = models.FloatField()


class Audience(models.Model):
    timestamp = models.IntegerField()
    channel = models.ForeignKey(Channel)
    value = models.IntegerField(default=0)

    class Meta:
        unique_together = (('timestamp', 'channel',),)
