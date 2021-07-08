from datetime import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core import exceptions
from django.db import connection
from django.http.response import HttpResponse
from django.utils.crypto import get_random_string
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.views import generic

from order.models import Order, OrderCar, ShopCart
from order.forms import CreateOrderForm

from user.models import User
from car.models import Car


class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    def post(self, request, id):
        user = User.objects.raw(f'SELECT * FROM user_user WHERE id = {request.user.id}')[0]

        if user.type_user == 1:
            checkproduct = ShopCart.objects.raw(
                f"SELECT * FROM order_shopcart WHERE car_id = {id}")

            if checkproduct:
                control = 1
            else:
                control = 0

            if control == 1:
                data = ShopCart.objects.raw(
                    f"SELECT * FROM order_shopcart WHERE car_id = {id}")[0]
                data.quantity += int(request.POST.get('quantity'))
                data.save()
                return HttpResponseRedirect('/cart')
            else:
                data = ShopCart()
                data.user_id = request.user.id
                data.car_id = id
                data.quantity = int(request.POST.get('quantity'))
                data.save()
                messages.success(request, 'Carro adicionado a sua conta')
                return HttpResponseRedirect('/cart')
        else: 
            messages.warning(request, 'Você é um locatário!')
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


class DeleteCartView(generic.DeleteView):
    def post(self, request, *args, **kwargs):
        try:
            with connection.cursor() as cursor:
                id = kwargs['pk']
                cursor.execute(
                    'DELETE FROM order_shopcart WHERE id = %s', [id])
                return HttpResponseRedirect('/cart')
        except Exception as error:
            return HttpResponse(error)


class CreateOrderView(generic.CreateView):
    template_name = "order_form.html"

    def get(self, request, *args, **kwargs):
        # form = self.form_class(request.POST)
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity

        context = {
            'total': total,
            'user': user,
            # 'form': form,
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

                cursor.execute(
                    'DELETE FROM order_shopcart WHERE user_id = %s', [request.user.id])


            return render(request, 'order_completed.html', { 'ordercode': code})
        except Exception as error:
            raise ValidationError(error)
