from django.contrib import admin
from order.models import Order, ShopCar, OrderCar


# Register your models here.
admin.site.register(Order)
admin.site.register(ShopCar)
admin.site.register(OrderCar)