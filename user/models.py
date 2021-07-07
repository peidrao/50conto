from django.db import models
from django.contrib.auth.models import AbstractUser
from modelAbs import ModelAbs

class User(AbstractUser, ModelAbs):
    TYPE_USER = (
        (1, 'Cliente'),
        (2, 'Locatário'),
    )

    GENDER_USER = (
        (1, 'Homem'),
        (2, 'Mulher'),
        (3, 'Outro'),   
    )

    STATUS_ACCOUNT = (
        (1, 'Verificada'),
        (2, 'Avaliação'),
        (3, 'Rejeitada'),        
    )

    # user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    username = models.CharField(unique=True, max_length=20, null=True, blank=False)
    email = models.CharField(unique=True, max_length=20, null=True, blank=False)
    # email = models.CharField(unique=True, max_length=50, null=True, blank=False)
    first_name = models.CharField(max_length=50, null=True, blank=False)
    last_name = models.CharField(max_length=50, null=True, blank=False)
    # cpf = models.CharField(unique=True, max_length=11, null=True, blank=False)
    status_account = models.IntegerField(choices=STATUS_ACCOUNT, null=True, default=2)
    type_user = models.IntegerField(choices=TYPE_USER, null=True)
    # gender_user = models.IntegerField(choices=GENDER_USER, null=True)
    email = models.EmailField(max_length=254, unique=True)
    REQUIRED_FIELDS = ('username',)
    USERNAME_FIELD = 'email'
    
    
    def __str__(self):
        return self.email

    # def user_name(self):
    #     return self.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '
