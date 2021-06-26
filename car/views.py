from django.shortcuts import render
from django.views.generic import DetailView

from car.models import Car

# Create your views here.
class CarDetailView(DetailView):
    model = Car
    template_name = "car_detail.html"