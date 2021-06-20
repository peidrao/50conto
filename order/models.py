from django.db import models
from django.db.models.deletion import CASCADE
from modelAbs import ModelAbs
from user.models import User
from car.models import Car

# Create your models here.
class Order(ModelAbs):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  car = models.ForeignKey(Car, on_delete=models.CASCADE)

  def __str__(self) -> str:
      return self.car.title