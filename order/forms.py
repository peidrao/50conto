from django.db.models import fields
from order.models import Order, ShopCart
from django import forms


class ShopCartForm(forms.ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class CreateOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'city', 'state_order', 'number', 'zip_code' ]
        