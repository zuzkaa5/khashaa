# -*-coding: utf-8 -*-
from django.contrib import admin
from khashaa.models import Coffee

# Register your models here.
class CoffeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'machid', 'orderid',  'price', 'qprice', 'code', 'timestamp'  )


admin.site.register(Coffee, CoffeeAdmin)