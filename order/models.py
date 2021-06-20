from django.db import models
from django.db.models.deletion import CASCADE
from modelAbs import ModelAbs
from user.models import User
from car.models import Car

# Create your models here.
class Order(ModelAbs):
  STATUS_ORDER = (
      (1, 'Accepted'),
      (2, 'Available'),
      (3, 'Not_Available'),
      (4, 'Canceled'),
  )
  STATE_ORDER = (
      (1, 'AC'),
      (2, 'AL'),
      (3, 'AP'),
      (4, 'AM'),
      (5, 'BA'),
      (6, 'CE'),
      (7, 'ES'),
      (8, 'GO'),
      (9, 'MA'),
      (10, 'MT'),
      (11, 'MS'),
      (12, 'MG'),
      (13, 'PA'),
      (14, 'PB'),
      (15, 'PR'),
      (16, 'PE'),
      (17, 'PI'),
      (18, 'RJ'),
      (19, 'RN'),
      (20, 'RS'),
      (21, 'RO'),
      (22, 'RR'),
      (23, 'SC'),
      (24, 'SP'),
      (25, 'SE'),
      (26, 'TO'),
      (27, 'DF'),
  )
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  car = models.ForeignKey(Car, on_delete=models.CASCADE)
  total = models.FloatField(null=False)
  status_order = models.IntegerField(choices=STATUS_ORDER, null=False)
  first_name = models.CharField(max_length=50, null=False, blank=False)
  last_name = models.CharField(max_length=50, null=False, blank=False)
  city = models.CharField(max_length=75, null=False, blank=False)
  state_order = models.IntegerField(choices=STATE_ORDER, null=False)
  address = models.CharField(max_length=250, null=False, blank=False)
  number = models.CharField(max_length=11, null=False, blank=False, verbose_name='Nº telefone celular')

  def __str__(self) -> str:
      return self.car.title

  