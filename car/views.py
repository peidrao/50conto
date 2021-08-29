import pdb
from django.shortcuts import render
from django.views.generic import DetailView

from car.models import Car
from order.models import Order, Review

# Create your views here.
class CarDetailView(DetailView):
    template_name = "car_detail.html"

    def get(self, request, *args, **kwargs):

        car = Car.objects.raw('SELECT * FROM car_car WHERE id = %s', [kwargs['pk']])[0]
        # reviews = Review.objects.raw('SELECT * FROM order_review WHERE car_id = %s', [kwargs['pk']])
        # import pdb ; pdb.set_trace()
        context = {
            'car': car,
            # 'reviews': reviews
        }

        return render(request, self.template_name, context)