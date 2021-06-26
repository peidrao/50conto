from car.models import Car
from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.

class HomeListView(ListView):
    model = Car
    template_name = 'index.html'

    def get_queryset(self):
       return super(HomeListView, self).get_queryset().filter(status_car=1)


