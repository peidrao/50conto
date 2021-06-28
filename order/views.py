from django import contrib
from car.models import Car
from user.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.crypto import get_random_string
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.shortcuts import render
from django.views import generic

from order.forms import CreateOrderForm, ShopCartForm
from order.models import Order, OrderCar, ShopCart

class AddCartInShopCartView(SuccessMessageMixin, generic.View):
    form_class = ShopCartForm
    
    def post(self, request, id):
        checkproduct = ShopCart.objects.filter(car_id=id)
        if checkproduct:
            control = 1
        else:
            control = 0

        form = self.form_class(request.POST)
        
        if form.is_valid():
            if control == 1:
                data = ShopCart.objects.get(car_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else:
                data = ShopCart()
                data.user_id = request.user.id
                data.car_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
            messages.success(request, 'Carro adicionado a sua conta')
            return HttpResponseRedirect('/cart')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/cart')

    def form_valid(self, form):
        form.instance.relates_to = ShopCart.objects.get(pk=self.kwargs.get("pk"))
        return super().form_valid(form)


class CartView(generic.View): 
    model = ShopCart
    template_name = 'cart.html'

    def get(self, request, *args, **kwargs):
        shopcart = ShopCart.objects.filter(user_id=self.request.user.id)
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity

        context = {
            'shopcart': shopcart,
            'total': total
        }

        return render(request, self.template_name, context)

    
class DeleteCartView(generic.DeleteView):
    model = ShopCart
    success_url ="/cart"


class CreateOrderView(generic.CreateView):
    template_name = "order_form.html"
    form_class = CreateOrderForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        user = User.objects.get(id=request.user.id)
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity

        context = {
            'total': total,
            'user': user,
            'form': form,
            'list': Order
        }

        # import pdb;pdb.set_trace()

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        shopcart = ShopCart.objects.filter(user_id=request.user.id)
        # car = Car.objects.get(user_id=request.user.id)
        
        total = 0
        for cart in shopcart:
            total = cart.car.price_day * cart.quantity
        if form.is_valid():
            data = Order()
            
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.address = form.cleaned_data['address']
            data.state_order = form.cleaned_data['state_order']
            data.city = form.cleaned_data['city']
            data.number = form.cleaned_data['number']
            data.zip_code = form.cleaned_data['zip_code']
            data.user_id = request.user.id
            data.total = total
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()
            for rs in shopcart:
                detail = OrderCar()
               
                detail.order_id = data.id
                detail.car_id = rs.car.id
                detail.user_id = request.user.id
                detail.quantity = rs.quantity
                detail.price = rs.price
                detail.save()

                car = Car.objects.get(id=rs.car_id)
                car.status_car = 2
                car.save()
            ShopCart.objects.filter(user_id=request.user.id).delete()

            # request.session['cart_items'] = 0

            messages.success(
                request, 'Your order has been completed, Thank You')

            context = {
                'ordercode': ordercode,
            }

            return render(request, 'order_completed.html', context)
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/order/orderbook')

            
