from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.dateparse import parse_date
from django.views import generic

from car.models import Car
from order.models import Order, ShopCart
from user.models import User
from .forms import ShopCartForm, CreateOrderForm


class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    form_class = ShopCartForm

    def post(self, request, id):
        try:
            user = User.objects.get(id=id)
            if user.type_user == 1:
                form = self.form_class(request.POST)

                if form.is_valid():
                    rent_to = request.POST['rent_to']
                    rent_from = request.POST['rent_from']

                    quantity = abs((parse_date(rent_to) - parse_date(rent_from)).days)
                    cart = form.save(commit=False)
                    cart.car_id = self.kwargs['id']
                    cart.user_id = request.user.id
                    cart.quantity = quantity
                    cart.save()

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

        try:
            shopcart = ShopCart.objects.get(user_id=request.user.id)
            total = shopcart.car.price_day * shopcart.quantity

            context = {
                'shopcart': shopcart,
                'total': total
            }

            return render(request, self.template_name, context)
        except:
            return render(request, self.template_name, {'shopcart': 0})

    def post(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.get(user_id=request.user.id)
        total = shopcart.car.price_day * shopcart.quantity

        if total == 0:
            messages.warning(request, 'Você precisa de pelo menos um carro adicionado para prosseguir!')
            return HttpResponseRedirect(f'/cart/')
        else:
            return HttpResponseRedirect(f'/order/')


class DeleteCartView(generic.DeleteView):
    model = ShopCart
    success_url = "/"


class CreateOrderView(generic.CreateView):
    template_name = "order_form.html"
    form_class = CreateOrderForm

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
            form = self.form_class(request.POST)
            if form.is_valid():
                order = form.save(commit=False)
                code = get_random_string(5).upper()
                order.total = shopcart.car.price_day * shopcart.quantity
                order.ordercode = code

                car = Car.objects.get(id=shopcart.car.id)
                car.status_car = 2

                car.save()
                shopcart.delete()

                return render(request, 'order_completed.html', {'ordercode': code})
        except:
            messages.warning(request,
                             'Ouve algum problema na finalização do aluguel, verifique se \
                              falta algum campo ser preenchido!')
            return HttpResponseRedirect('/order')
