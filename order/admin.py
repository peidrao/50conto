from django.contrib import admin
from order.models import Order, ShopCart, OrderCar


# Register your models here.
admin.site.register(Order)
admin.site.register(ShopCart)
admin.site.register(OrderCar)