
from datetime import date
import datetime
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import connection
from django.http.response import HttpResponse

from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy

from order.models import CreditCard, Order, Payment, ShopCart

from user.models import User
from car.models import Car


class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    def post(self, request, id):
        if not request.user.is_anonymous:
            user = User.objects.raw(f'SELECT * FROM user_user WHERE id = {request.user.id}')[0]
            if user.type_user == 1:
                ativo = 1
                rent_from = request.POST['rent_from']
                rent_to = request.POST['rent_to']
                user_id = request.user.id
                car_id = self.kwargs['id']
                car_object = Car.objects.raw('SELECT * FROM car_car WHERE id = %s', [car_id])[0]

                rent_to_parser = datetime.datetime.strptime(rent_to, "%Y-%m-%d").date()
                rent_from_parser = datetime.datetime.strptime(rent_from, "%Y-%m-%d").date()

                shopcart = ShopCart.objects.raw('SELECT * FROM order_shopcart cart WHERE cart.car_id = %s', [id])[:]

                for cart in shopcart:
                    if cart.rent_from == rent_from_parser or cart.rent_to == rent_to_parser:
                        messages.warning(request, 'Você não pode alugar o carro pois ele já está alugado para está data')
                        return HttpResponseRedirect(f'/car_detail/{id}')


                if rent_from_parser < car_object.initial_date or rent_to_parser > car_object.finish_date:
                    messages.warning(request, 'Você não pode alugar o carro para em uma data indisponível')
                    return HttpResponseRedirect(f'/car_detail/{id}')


                with connection.cursor() as cursor:
                    cursor.execute("INSERT INTO order_shopcart VALUES(%s, %s, %s, %s, %s, %s)",[
                    None, rent_from, rent_to, car_id, user_id, ativo
                ])
                messages.success(request, 'Carro adicinado no carrinho com sucesso!')
                return HttpResponseRedirect(reverse_lazy('order:cart'))

            else:
                messages.warning(request, 'Você é um locatário!')
                return HttpResponseRedirect(f'/car_detail/{id}')
        else:
            messages.warning(request, 'Você precisa logar em uma conta!')
            return HttpResponseRedirect(f'/car_detail/{id}')



class CartView(generic.View):
    model = ShopCart
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.raw(
            f'SELECT * FROM order_shopcart WHERE user_id = {request.user.id} and ativo = 1')

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
            f'SELECT * from order_shopcart ORDER by id DESC  LIMIT 1')


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

        try:
            # shopcart = ShopCart.objects.filter(user_id=request.user.id).order_by('-id')[0]
            shopcart = ShopCart.objects.raw('SELECT * FROM order_shopcart shop  WHERE shop.user_id = %s ORDER BY shop.id DESC LIMIT 1', [request.user.id])[0]


            status_order = 1
            payment_type = 1
            total_price = shopcart.price * shopcart.day_quantity

            number_cart = request.POST['cart_number']
            name_cart = request.POST['name']
            code_cart = request.POST['security_number']
            expiration_cart = request.POST['expirate_date']


            with connection.cursor() as credit_card:
                credit_card.execute("INSERT INTO order_creditcard VALUES(%s, %s, %s, %s, %s)",[
                    None, expiration_cart, number_cart, code_cart, name_cart
                ])

            # last_card = CreditCard.objects.last()
            last_card = CreditCard.objects.raw('SELECT * FROM order_creditcard credit_card ORDER BY credit_card.id DESC LIMIT 1')[0]


            with connection.cursor() as payment:
                payment.execute("INSERT INTO order_payment VALUES(%s, %s, %s)",[
                    None, payment_type, last_card.id
                ])

            # last_payment = Payment.objects.last()
            last_payment = Payment.objects.raw('SELECT * FROM order_payment payment ORDER BY payment.id DESC LIMIT 1')[0]

            with connection.cursor() as order:
                order.execute("INSERT INTO order_order VALUES(%s, %s, %s, %s, %s, %s)",[
                    None, status_order, total_price, shopcart.id, last_payment.id, request.user.id
                ])

            # with connection.cursor() as cursor_update:
            #     cursor_update.execute("UPDATE order_shopcart SET ativo = 0 WHERE id = %s",[
            #         shopcart.id
            #     ])

            return render(request, 'order_completed.html', {})
        except Exception as error:
            messages.warning(request, 'Ouve algum problema na finalização do aluguel, verifique se falta algum campo ser preenchido!')
            return HttpResponseRedirect('/order')


