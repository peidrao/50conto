from django import forms

from order.models import Order, ShopCart
from .validators import OrderValidator


class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ('rent_to', 'rent_from')


class CreateOrderForm(forms.ModelForm):
    zip_code = forms.CharField(validators=[OrderValidator.zipcode_validation])
    # expiration_cart = forms.CharField(validators=[OrderValidator.expirationcard_validation])

    def __init__(self, *args, **kargs):
        super(CreateOrderForm, self).__init__(*args, **kargs)

    class Meta:
        model = Order
        fields = (
            'first_name', 'last_name', 'address', 'city', 'state_order', 'number', 'zip_code',
            'code_cart', 'expiration_cart', 'name_cart', 'number_cart'
        )
