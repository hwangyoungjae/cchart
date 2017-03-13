from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Code(models.Model):
    code = models.CharField(max_length=10, primary_key=True, null=False, blank=False)

class Stock(models.Model):
    code = models.ForeignKey(Code)
    date = models.DateTimeField(blank=False, null=True, default=0)
    open = models.FloatField(blank=False, null=True, default=0)
    high = models.FloatField(blank=False, null=True, default=0)
    low = models.FloatField(blank=False, null=True, default=0)
    close = models.FloatField(blank=False, null=True, default=0)
    adjclose = models.FloatField(blank=False, null=True, default=0)
    volume = models.IntegerField(blank=False, null=True, default=0)
    def __unicode__(self):
        return str(self.date)

class History(models.Model):
    sco_ip = models.CharField(max_length=15)
    sco_datetime = models.DateTimeField(auto_now_add=True)
    sco_referer = models.URLField(null=True, blank=True, default='')
    sco_current = models.URLField(null=True, blank=True, default='')
    sco_agent = models.CharField(max_length=1024, null=True, blank=True, default='')
    sco_method = models.CharField(max_length=6, null=True, blank=True, default='')







