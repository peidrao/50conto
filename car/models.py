from django.db.models.aggregates import Avg, Count
from modelAbs import ModelAbs
from user.models import User
from django.db import models
# Create your models here.
from user.models import User


class Car(ModelAbs):
    STATUS_CAR = (
        (1, 'Ativado'),
        (2, 'Desativado'),
          
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price_day = models.DecimalField(max_digits=6, decimal_places=2)
    image_car = models.ImageField(upload_to="media", null=True, blank=True)
    description = models.TextField(null=False, blank=False)
    carName = models.CharField(max_length = 20,null=True, blank=False)
    plaque = models.CharField(max_length = 10,null=True, blank=False)
    car_model = models.CharField(max_length = 20,null=True, blank=False)
    color = models.CharField(max_length = 20,null=True, blank=False)
    #alterar para inteiro
    vehicle_year = models.IntegerField(null=True)
    mileage = models.CharField(max_length = 20,null=True, blank=False)
    status_car = models.IntegerField(choices=STATUS_CAR,null=False)
    initial_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)

    def __str__(self):
        return f'MODELO: {self.car_model} - COR: {self.color}'

    
    @property
    def day(self):
        return abs((self.finish_date - self.initial_date).days)
    
    @property
    def general_rate(self):
        reviews = Review.objects.filter(car=self, status_read=1).aggregate(avarage=Avg('rate'))
        avg = 0
        if reviews['avarage'] is not None:
            avg = float(reviews['avarage'])
        return avg

    @property
    def count_reviews(self):
        reviews = Review.objects.filter(
            car=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews['count'] is not None:
            ctn = int(reviews['count'])
        return ctn



    

class ImageCar(ModelAbs):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    title = models.CharField(max_length=50, null=False, blank=False)
    image = models.ImageField(upload_to='media')

class Review (ModelAbs):
    STATUS = (
    (1, 'Lida'),
    (2, 'Não Lida'),
)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title =  models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    rate = models.IntegerField(default=1)
    status_read = models.IntegerField(choices=STATUS, default=2)

    def __str__(self) -> str:
        return self.user.first_name

