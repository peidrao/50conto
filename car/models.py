from modelAbs import ModelAbs
from django.db import models
# Create your models here.

class Car(ModelAbs):
    title = models.CharField(max_length=50, null=False, blank=False)


class ImageCar(ModelAbs):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)