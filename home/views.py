from car.models import Car
from django.shortcuts import render
from django.views.generic import ListView
# Create your views here.

class HomeListView(ListView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        car = Car.objects.raw("SELECT * FROM car_car WHERE status_car = 1")
        return render(request, self.template_name, {'object_list':  car})

