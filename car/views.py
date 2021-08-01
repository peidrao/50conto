from django.shortcuts import render
from django.views.generic import DetailView

from car.models import Car
from order.models import Order, Review


class CarDetailView(DetailView):
    template_name = "car_detail.html"

    def get(self, request, *args, **kwargs):
        car = Car.objects.get(id=kwargs['pk'])
        reviews = Review.objects.filter(car_id=car.id)
        ranted_car = Order.objects.filter(car_id=car.id)

        context = {
            'car': car,
            'reviews': reviews,
            'ranted': ranted_car
        }

        return render(request, self.template_name, context)
