from django.db import models
from modelAbs import ModelAbs
from user.models import User

# Create your models here.


class Order(ModelAbs):
    STATUS_ORDER = (
        (1, 'Pagamento em processamento'),
        (2, 'Aguardando pagamento'),
        (3, 'Pagamento feito'),
        (4, 'Cancelar'),
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
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE)

    status_order = models.IntegerField(
        choices=STATUS_ORDER, null=True, default=1)
    
    # personal information
    first_name = models.CharField(max_length=50, null=False, blank=False)
    last_name = models.CharField(max_length=50, null=False, blank=False)

    # address 
    city = models.CharField(max_length=75, null=False, blank=False)
    state_order = models.IntegerField(choices=STATE_ORDER, null=False)
    address = models.CharField(
        'Endereço', max_length=250, null=False, blank=False)
    number = models.CharField('Nº telefone celular',
                              max_length=11, null=False, blank=False)
    zip_code = models.CharField('CEP', max_length=11, null=False, blank=False)

    code = models.CharField('Código', max_length=11, null=False, blank=False)
    
    total = models.FloatField(null=False)

    # payment
    number_cart = models.CharField(max_length=16, null=False)
    name_cart = models.CharField(max_length=30, null=False)
    code_cart = models.CharField(max_length=3, null=False)
    expiration_cart = models.CharField(max_length=5, null=False)

    def __str__(self) -> str:
        return self.zip_code


class ShopCart(ModelAbs):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey("car.Car", on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False)

    rent_from = models.DateField(null=True)
    rent_to = models.DateField(null=True)

    @property
    def price(self):
        return (self.car.price_day)

    def __str__(self) -> str:
        return self.car.car_model



class Review (ModelAbs):
    STATUS = (
        (1, 'Não Lida'),
        (1, 'Aprovado'),
        (3, 'Reprovado'),
    )

    car = models.ForeignKey("car.Car", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    title = models.CharField(max_length=100, blank=True)
    subject = models.CharField(max_length=100, blank=True)
    comment = models.CharField(max_length=255, blank=True)

    rate = models.IntegerField(default=1)
    status_read = models.IntegerField(choices=STATUS, default=1)

    def __str__(self) -> str:
        return self.user.first_name