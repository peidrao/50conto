from order.models import Order
from django import forms
# from django.contrib.auth.models import User

from car.models import Car, Review


class RegisterCarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ('carName', 'plaque', 'car_model', 'color', 'image_car', 'price_day', 'description',
                  'vehicle_year', 'mileage', 'status_car', 'initial_date', 'finish_date', )


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('carName', 'plaque', 'car_model', 'color', 'image_car', 'price_day', 'description',
                  'vehicle_year', 'mileage', 'status_car', 'initial_date', 'finish_date', )


class RateCarUserForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
