from django.db import models
from user.models import User

from django.utils.dateparse import parse_date

# Create your models here.


class Order(models.Model):
    STATUS_ORDER = (
        (1, 'Pagamento em processamento'),
        (2, 'Aguardando pagamento'),
        (3, 'Pagamento feito'),
        (4, 'Cancelar'),
    )

    payment = models.ForeignKey(
        "order.Payment", on_delete=models.CASCADE, null=False, blank=False)
    cart = models.ForeignKey(
        "order.ShopCart", on_delete=models.CASCADE, null=False, blank=False)

    status_order = models.IntegerField(
        choices=STATUS_ORDER, null=True, default=1)

    total = models.FloatField(null=False)

    def __str__(self) -> str:
        return f'Nome cliente: {self.cart.user.first_name}'


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE)

    rent_from = models.DateField(null=True)
    rent_to = models.DateField(null=True)

    @property
    def day_quantity(self):
        return abs((parse_date(self.rent_to)-parse_date(self.rent_from)).days)

    @property
    def price(self):
        return (self.car.price_day)

    def __str__(self) -> str:
        return self.car.car_model


class Review (models.Model):
    STATUS = (
        (1, 'Não Lida'),
        (1, 'Aprovado'),
        (3, 'Reprovado'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    rate = models.IntegerField(default=1)
    status_read = models.IntegerField(choices=STATUS, default=1)

    def __str__(self) -> str:
        return self.user.first_name


class CreditCard(models.Model):
    expirate_date = models.CharField(max_length=100)
    cart_number = models.CharField(max_length=100)
    security_number = models.CharField(max_length=3)
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return 'Nome do titular: {self.name}'


class Payment(models.Model):
    PAYMENT_TYPE = (
        (u'1', 'Cartão de Crédito')
        (u'2', 'Espécie')
    )
    credit_card = models.ForeignKey(
        CreditCard, on_delete=models.CASCADE, blank=True, null=True)
    payment_type = models.CharField(choices=PAYMENT_TYPE, max_length=100)
