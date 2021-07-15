from car.models import Car
from django.shortcuts import render
from django.views import generic
# Create your views here.

class HomeListView(generic.ListView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        car = Car.objects.raw("SELECT * FROM car_car WHERE status_car = 1")
        return render(request, self.template_name, {'object_list':  car})


class SearchCarView(generic.TemplateView):
    template_name = 'pages/search_car.html'
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('search_car', '')

        cars  = Car.objects.raw(f'SELECT * FROM car_car WHERE car_model LIKE "%{name}%"')
    
        return render(request, self.template_name, {'cars': cars})


        