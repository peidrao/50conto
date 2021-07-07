from order.models import Order
from django import forms
# from django.contrib.auth.models import User

from car.models import Car, Review




class RateCarUserForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("subject", "title", "comment", "rate",)
