# -*-coding: utf-8 -*-
from django.db import models
import datetime

# Create your models here.

class Coffee(models.Model):
    ver = models.CharField(max_length=50)
    orderid = models.CharField(max_length=62)
    machid = models.CharField(max_length=100)
    trackno = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    price = models.IntegerField()
    qprice = models.IntegerField(default=0)
    channelid = models.PositiveIntegerField()
    randstr = models.CharField(max_length=200)
    #timestamp = models.DateTimeField()
    timestamp = models.CharField()
    sign = models.CharField(max_length=300)

    torderid = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True) # True - success, False - failure
    errinfo = models.TextField(null=True, blank=True)

    code = models.IntegerField(default=2) # 0 - failure, 1 - success, 2 - waiting payment, 3 - tran expired, 4 - tran closed, 5 - completed

    qpay_invoice_id = models.CharField(max_length=300)
    access_token = models.CharField(max_length=200, null=True)


    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "Coffee"
        verbose_name_plural = "Coffee"
