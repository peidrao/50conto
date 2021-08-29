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
from order.models import CreditCard, Order, Payment, ShopCart

from user.models import User
from car.models import Car


class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    def post(self, request, id):
        try:
            # import pdb ; pdb.set_trace()
            user = User.objects.raw(f'SELECT * FROM user_user WHERE id = {request.user.id}')[0]
            if user.type_user == 1:

                rent_from = request.POST['rent_from']
                rent_to = request.POST['rent_to']
                user_id = request.user.id
                car_id = self.kwargs['id']

                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO order_shopcart VALUES(%s, %s, %s, %s, %s)",[
                    None, rent_from, rent_to, car_id, user_id
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
            total = cart.car.price_day * cart.day_quantity


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
            total = cart.car.price_day * cart.day_quantity
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
        shopcart = ShopCart.objects.raw(
            f'SELECT * FROM order_shopcart WHERE user_id = {request.user.id}')

        user = User.objects.raw(f'SELECT id FROM user_user WHERE id = {request.user.id}')

        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.day_quantity

        context = {
            'total': total,
            'user': user,
            'list': Order
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # import pdb ; pdb.set_trace()
        try:
            shopcart = ShopCart.objects.get(user_id=request.user.id)
            # shopcart = ShopCart.objects.raw(f'SELECT * FROM order_shopcart WHERE user_id = {request.user.id}')

            status_order = 1
            payment_type = 1
            total_price = shopcart.price * shopcart.day_quantity
            # TODO: Criar cartão
            # TODO: Criar forma de pagamento
            # TODO: Criar pedido

            number_cart = request.POST['cart_number']
            name_cart = request.POST['name']
            code_cart = request.POST['security_number']
            expiration_cart = request.POST['expirate_date']

            # import pdb ; pdb.set_trace()

            with connection.cursor() as credit_card:
                credit_card.execute("INSERT INTO order_creditcard VALUES(%s, %s, %s, %s, %s)",[
                    None, expiration_cart, number_cart, code_cart, name_cart
                ])

            last_cart = CreditCard.objects.last()

            with connection.cursor() as payment:
                payment.execute("INSERT INTO order_payment VALUES(%s, %s, %s)",[
                    None, payment_type, last_cart.id
                ])

            last_payment = Payment.objects.last()

            with connection.cursor() as order:
                order.execute("INSERT INTO order_order VALUES(%s, %s, %s, %s, %s)",[
                    None, status_order, total_price, shopcart.id, last_payment.id
                ])

            return render(request, 'order_completed.html', {})
        except Exception:
            messages.warning(request, 'Ouve algum problema na finalização do aluguel, verifique se falta algum campo ser preenchido!')
            return HttpResponseRedirect('/order')

