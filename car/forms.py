from django import forms
# from django.contrib.auth.models import User

from car.models import Car


class RegisterCarForm(forms.ModelForm):

    class Meta:
        model = Car
        fields = ('carName', 'plaque', 'car_model', 'color', 'image_car',
                  'vehicle_year', 'mileage', 'status_car', 'initial_date', 'finish_date', )


class CarUpdateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('carName', 'plaque', 'car_model', 'color', 'image_car',
                  'vehicle_year', 'mileage', 'status_car', 'initial_date', 'finish_date', )