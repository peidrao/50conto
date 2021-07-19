from django.shortcuts import render
from django.views.generic import DetailView

from car.models import Car
from order.models import Order, Review

# Create your views here.
class CarDetailView(DetailView):
    template_name = "car_detail.html"

    def get(self, request, *args, **kwargs):
        car = Car.objects.raw('SELECT * FROM car_car WHERE id = %s', [kwargs['pk']])[0]
        reviews = Review.objects.raw('SELECT * FROM order_review WHERE car_id = %s', [kwargs['pk']])
        ranted_car = Order.objects.raw('SELECT * FROM order_order WHERE car_id = %s ORDER BY id DESC LIMIT 1', [kwargs['pk']])[0]

        context = {
            'car': car,
            'reviews': reviews,
            'ranted': ranted_car
        }

        return render(request, self.template_name, context)