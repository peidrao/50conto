from django.contrib import admin
from order.models import Order, ShopCart

# Register your models here.
admin.site.register(Order)
admin.site.register(ShopCart)