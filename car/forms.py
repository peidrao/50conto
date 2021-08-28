from django import forms
# from django.contrib.auth.models import User

from car.models import Car, Review


class RateCarUserForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ("subject", "title", "comment", "rate",)


class RegisterCarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ('plaque', 'car_model', 'color', 'brand', 'image_car', 'price_day',
                 'status_car', 'initial_date', 'finish_date')
