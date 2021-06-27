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
      (1, 'AC - Acre'),
      (2, 'AL - Alagoas'),
      (3, 'AP - Amapá'),
      (4, 'AM - Amazonas'),
      (5, 'BA - Bahia'),
      (6, 'CE - Ceará'),
      (7, 'DF - Distrito Federal'),
      (8, 'ES - Espírito Santo'),
      (9, 'GO - Goiás'),
      (10, 'MA - Maranhão'),
      (11, 'MT - Mato Grosso'),
      (12, 'MS - Mato Grosso do Sul'),
      (13, 'MG - Minas Gerais'),
      (14, 'PA - Pará'),
      (15, 'PB - Paraíba'),
      (16, 'PR - Paraná'),
      (17, 'PE - Pernambuco'),
      (18, 'PI - Piauí'),
      (19, 'RJ - Rio de Janeiro'),
      (20, 'RN - Rio Grande do Norte'),
      (21, 'RS - Rio Grande do Sul'),
      (22, 'RO - Rondônia'),
      (23, 'RR - Roraima'),
      (24, 'SC - Santa Catarina'),
      (25, 'SP - São Paulo'),
      (26, 'SE - Sergipe'),
      (27, 'TO - Tocantins'),
  )
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
#   car = models.ForeignKey(Car, on_delete=models.CASCADE)
  total = models.FloatField(null=False)
  status_order = models.IntegerField(choices=STATUS_ORDER, null=True, default=2)
  first_name = models.CharField(max_length=50, null=False, blank=False)
  last_name = models.CharField(max_length=50, null=False, blank=False)
  city = models.CharField(max_length=75, null=False, blank=False)
  state_order = models.IntegerField(choices=STATE_ORDER, null=False)
  address = models.CharField('Endereço', max_length=250, null=False, blank=False)
  number = models.CharField('Nº telefone celular', max_length=11, null=False, blank=False)
  zip_code  = models.CharField('CEP', max_length=11, null=False, blank=False)
  code = models.CharField('CEP', max_length=11, null=False, blank=False)

  def __str__(self) -> str:
      return self.zip_code


class ShopCart(ModelAbs):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  car = models.ForeignKey(Car, on_delete=models.CASCADE)  
  quantity = models.IntegerField(null=False)
  
  @property
  def price(self):
      return (self.car.price_day)

  def __str__(self) -> str:
      return self.car.carName


class OrderCar(ModelAbs):

  user = models.ForeignKey(User, on_delete=models.CASCADE)
  car = models.ForeignKey(Car, on_delete=models.CASCADE)  
  order = models.ForeignKey(Order, on_delete=models.CASCADE) 
  quantity = models.IntegerField(null=False, blank=False)
  price = models.FloatField(null=False, blank=False)

  def __str__(self) -> str:
      return self.car.carName