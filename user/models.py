from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser, models.Model):
    TYPE_USER = (
        (1, 'Cliente'),
        (2, 'Locatário'),
    )

    STATUS_ACCOUNT = (
        (1, 'Verificada'),
        (2, 'Avaliação'),
        (3, 'Rejeitada'),
    )

    GENDER = (
        (1, 'Masculino'),
        (2, 'Feminino'),
        (3, 'Outro'),
    )

    username = models.CharField(
        unique=True, max_length=20, null=True, blank=False)
    email = models.CharField(
        unique=True, max_length=20, null=True, blank=False)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    cpf = models.CharField(max_length=11, null=True, blank=False)
    gender = models.IntegerField(choices=GENDER, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=15)
    status_account = models.IntegerField(
        choices=STATUS_ACCOUNT, null=True, default=2)
    type_user = models.IntegerField(choices=TYPE_USER, null=True)
    email = models.EmailField(max_length=254, unique=True)

    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
