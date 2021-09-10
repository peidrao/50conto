import pdb
from django.shortcuts import render
from django.views.generic import DetailView
from django.db import connection


from car.models import Car
from order.models import Order, Review, ShopCart

# Create your views here.
class CarDetailView(DetailView):
    template_name = "car_detail.html"

    def get(self, request, *args, **kwargs):

        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(cart.id) from order_shopcart cart WHERE cart.car_id = %s', [kwargs['pk']])
        shopcart_count = cursor.fetchone()[0]

        shopcart = ShopCart.objects.raw('SELECT * FROM order_shopcart cart WHERE cart.car_id = %s', [kwargs['pk']])
        car = Car.objects.raw('SELECT * FROM car_car WHERE id = %s', [kwargs['pk']])[0]
        context = {
            'car': car,
            'shopcart': shopcart,
            'shopcart_count': shopcart_count
        }

        return render(request, self.template_name, context)


