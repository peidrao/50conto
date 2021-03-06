from django.db.models.aggregates import Avg, Count
from user.models import User
from order.models import Review
from django.db import models
from datetime import date


class Car(models.Model):
    STATUS_CAR = (
        (1, 'Ativado'),
        (2, 'Desativado'),
        (3, 'Alugado'),
    )

    BRAND = (
        (1, 'Outro'),
        (2, 'Volkswagen'),
        (3, 'Toyota'),
        (4, 'Nissan'),
        (5, 'Ford'),
        (6, 'Honda'),
        (7, 'Hyundai'),
        (8, 'Chevrolet'),
        (9, 'Mercedes-Benz'),
        (10, 'BMW'),
        (11, 'Tesla'),
    )

    COLOR = (
        (1, 'Outra'),
        (2, 'Branco'),
        (3, 'Preto'),
        (4, 'Prata'),
        (5, 'Cinza'),
        (6, 'Vermelho'),
        (7, 'Azul'),
        (8, 'Marrom'),
        (9, 'Verde'),
        (10, 'Amarelo'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_car = models.TextField(null=True, blank=True)

    car_model = models.CharField(max_length=255, null=True, blank=False)
    brand = models.PositiveIntegerField(choices=BRAND, null=True, blank=False)
    plaque = models.CharField(max_length=10, null=True, blank=False)
    status_car = models.PositiveIntegerField(choices=STATUS_CAR, null=False)

    color = models.PositiveIntegerField(choices=COLOR, null=False)

    price_day = models.DecimalField(max_digits=6, decimal_places=2)

    initial_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'MODELO: {self.car_model} - COR: {self.color}'

    @property
    def days(self):
        return abs((self.finish_date - self.initial_date).days)

    @property
    def general_rate(self):
        reviews = Review.objects.filter(
            car=self, status_read=1).aggregate(avarage=Avg('rate'))
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

    @property
    def is_past_due(self):
        return  date.today() > self.finish_date
