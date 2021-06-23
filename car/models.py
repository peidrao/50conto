from modelAbs import ModelAbs
from user.models import User
from django.db import models
# Create your models here.
from user.models import User


class Car(ModelAbs):
    STATUS_CAR = (
        (1, 'ativado'),
        (2, 'desativado'),
          
    )
    user = models.name = models.ForeignKey(User, on_delete=models.CASCADE)
    image_car = models.ImageField(upload_to="media", null=True, blank=True)
    title = models.CharField(max_length=50, null=False, blank=False)
    carName = models.CharField(max_length = 20,null=True, blank=False)
    plaque = models.CharField(max_length = 10,null=True, blank=False)
    car_model = models.CharField(max_length = 20,null=True, blank=False)
    color = models.CharField(max_length = 20,null=True, blank=False)
    vehicle_year = models.DateField(null=True)
    mileage = models.CharField(max_length = 20,null=True, blank=False)
    status_car = models.IntegerField(choices=STATUS_CAR,null=False)
    initial_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)

    def __str__(self):
        return f'MODELO: {self.car_model} - COR: {self.color}'
    

class ImageCar(ModelAbs):
    car_id = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
