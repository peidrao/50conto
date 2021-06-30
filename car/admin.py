from django.contrib import admin
from car.models import Car, ImageCar, Review

# Register your models here.
admin.site.register(Car) 
admin.site.register(ImageCar)
admin.site.register(Review)
