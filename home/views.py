from car.models import Car
from django.shortcuts import render
from django.views.generic import View
# Create your views here.

class HomeView(View):
    model = Car
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        #import pdb;pdb.set_trace()
        return render(request, self.template_name, {})
