from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import connection
from django.http.response import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from django.utils.dateparse import parse_date
from order.models import Order, ShopCart

from user.models import User
from car.models import Car


class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    def post(self, request, id):
        try:
            user = User.objects.raw(f'SELECT * FROM user_user WHERE id = {request.user.id}')[0]
            if user.type_user == 1:

                rent_from = request.POST['rent_from']
                rent_to = request.POST['rent_to']
                user_id = request.user.id
                car_id = self.kwargs['id']

                created_at = datetime.now()
                updated_at = datetime.now()
                quantity = abs((parse_date(rent_to)-parse_date(rent_from)).days)

                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO order_shopcart VALUES(%s, %s, %s, %s, %s, %s, %s, %s)",[
                    None, created_at, updated_at, quantity, car_id, user_id, rent_from, rent_to
                ])
                messages.success(request, 'Carro adicinado no carrinho com sucesso!')
                return HttpResponseRedirect(reverse_lazy('order:cart'))
            else: 
                messages.warning(request, 'Você é um locatário!')
                return HttpResponseRedirect(f'/car_detail/{id}')
        except Exception as error:
            messages.warning(request, error)
            return HttpResponseRedirect(f'/car_detail/{id}')
            
            
class CartView(generic.View):
    model = ShopCart
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.raw(
            f'SELECT * FROM order_shopcart WHERE user_id = {request.user.id}')
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity

        context = {
            'shopcart': shopcart,
            'total': total
        }

        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.raw(
            f'SELECT * FROM order_shopcart WHERE user_id = {request.user.id}')
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity
        if total == 0:
            messages.warning(request, 'Você precisa de pelo menos um carro adicionado para prosseguir!')
            return HttpResponseRedirect(f'/cart/')
        else:
            return HttpResponseRedirect(f'/order/')


class DeleteCartView(generic.DeleteView):
    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                id = kwargs['pk']
                cursor.execute(
                    'DELETE FROM order_shopcart WHERE id = %s', [id])
            messages.success(request, 'Carro removido do carrinho!')    
            return HttpResponseRedirect('/cart')
        except Exception as error:
            return HttpResponse(error)


class CreateOrderView(generic.CreateView):
    template_name = "order_form.html"

    def get(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity

        context = {
            'total': total,
            'user': user,
            'list': Order
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            shopcart = ShopCart.objects.get(user_id=request.user.id)
            

            user_id = request.user.id
            car_id = shopcart.car.id
            status_order = 1
            total_price = shopcart.car.price_day * shopcart.quantity
            created_at = datetime.now()
            updated_at = datetime.now()
            code = get_random_string(5).upper()
            state_order = request.POST['state_order']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            city = request.POST['city']
            address = request.POST['address']
            number = request.POST['number']
            zip_code = request.POST['zip_code']

            number_cart = request.POST['number_cart']
            name_cart = request.POST['name_cart']
            code_cart = request.POST['code_cart']
            expiration_cart = request.POST['expiration_cart']

            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO order_order VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)",[
                    None, created_at, updated_at, total_price, first_name, last_name, city, state_order, address, number, zip_code, code, 
                    user_id, car_id, code_cart, expiration_cart, name_cart, number_cart, status_order
                ])

                cursor.execute('UPDATE car_car SET status_car = 2 WHERE id = %s', [car_id])

                cursor.execute(
                    'DELETE FROM order_shopcart WHERE user_id = %s', [request.user.id])

            return render(request, 'order_completed.html', { 'ordercode': code})
        except Exception:
            messages.warning(request, 'Ouve algum problema na finalização do aluguel, verifique se falta algum campo ser preenchido!')  
            return HttpResponseRedirect('/order')
            
