from datetime import datetime

from django.contrib.auth import authenticate, login as auth_login, logout as logout_func
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.db import connection
from django.views import generic

from car.forms import RateCarUserForm
from user.models import User
from car.models import Car, Review
from order.models import OrderCar

class LoginView(generic.View):
    template_name = 'login_user.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)

                return HttpResponseRedirect('/profile')
            else:
                return HttpResponse("Inactive user.")
        else:
            messages.warning(request, 'Erro! Lemail ou senha errados')
            return HttpResponseRedirect('/login')


class SignUpUserView(SuccessMessageMixin, generic.CreateView):
    template_name = 'register_user.html'

    def post(self, request):
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        email = request.POST["email"]
        last_name = request.POST["last_name"]
        type_user = request.POST["type_user"]
        password = request.POST["password1"]
        status_account = 2
        last_login = datetime.now()
        is_superuser = 0
        is_active = 1
        is_staff = 0
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_at = datetime.now()
        updated_at = datetime.now()

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_user VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)", [
                           None, make_password(password), last_login, is_superuser, is_staff, is_active, date_joined,
                           created_at, updated_at, username, first_name, last_name, type_user, email, status_account
            ])
            # new_user_id = cursor.lastrowid
            # print("New user id", new_user_id)

            return HttpResponseRedirect(reverse_lazy('home:index'))

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user_list': User})


class LogoutUserView(generic.View):
    def get(self, request):
        logout_func(request)
        return HttpResponseRedirect('/')


class ProfileUserView(generic.TemplateView):
    template_name = 'profile_user.html'


class UserCreateCarView(SuccessMessageMixin, generic.CreateView):
    template_name = 'register_car.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'car_options': Car})

    def post(self, request):
        plaque = request.POST["plaque"]
        car_model = request.POST["car_model"]
        color = request.POST["color"]
        image_car = request.POST["image_car"]
        price_day = request.POST["price_day"]
        description = request.POST["description"]
        vehicle_year = request.POST["vehicle_year"]
        brand = request.POST["brand"]
        status_car = request.POST["status_car"]
        initial_date = request.POST["initial_date"]
        finish_date = request.POST["finish_date"]
        created_at = datetime.now()
        updated_at = datetime.now()
        user_id = request.user.id

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO car_car VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)", [
                           None, created_at, updated_at, image_car, description, brand, status_car, color, car_model,
                           plaque, vehicle_year, price_day, initial_date, finish_date, user_id, ])

            return HttpResponseRedirect(reverse_lazy('home:index'))


class ListUserCarsView(generic.ListView):
    template_name = 'list_cars.html'

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        user = Car.objects.raw(f"SELECT * FROM car_car WHERE user_id = {pk}")
        context = {'car_list': user}

        return render(request, self.template_name, context)


class ListMyCarView(generic.ListView):
    template_name = 'my_car.html'
    context_object_name = "my_car"

    def get(self, request, *args, **kwargs):
        order_car = OrderCar.objects.raw(
            F'SELECT *  \
            FROM order_ordercar \
            WHERE user_id = {request.user.id}'
        )
    

        context = {'order_car': order_car}
        return render(request, self.template_name, context)

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = Car.objects.filter(user_id=pk)
        return user


class UpdateCarView(generic.UpdateView):
    template_name = "update_car.html"

    def get(self, request, *args, **kwargs):
        id = kwargs['pk']
        car = Car.objects.raw('SELECT * FROM car_car WHERE id=%s', [id])[0]
        context = {
            'car_update': car,
            'car_options': Car
        }

        return render(request, self.template_name, context)

    def post(self, request, pk=None):
        plaque = request.POST["plaque"]
        car_model = request.POST["car_model"]
        color = request.POST["color"]
        image_car = request.POST["image_car"]
        price_day = request.POST["price_day"]
        description = request.POST["description"]
        vehicle_year = request.POST["vehicle_year"]
        brand = request.POST["brand"]
        status_car = request.POST["status_car"]
        initial_date = request.POST["initial_date"]
        finish_date = request.POST["finish_date"]
        updated_at = datetime.now()
        user_id = request.user.id
        car_id = self.kwargs['pk']

        with connection.cursor() as cursor:
            cursor.execute("UPDATE car_car \
                            SET updated_at=%s, price_day=%s, description=%s, brand=%s, plaque=%s, \
                                car_model=%s, color=%s, vehicle_year=%s, status_car=%s, initial_date=%s, \
                                finish_date=%s, user_id=%s, image_car=%s \
                                WHERE id = %s", [
                           updated_at, price_day, description, brand, plaque, car_model, color, vehicle_year, 
                           status_car, initial_date, finish_date, user_id, image_car, car_id
                        ])

            return HttpResponseRedirect(reverse_lazy('home:index'))


class RateCarUserView(generic.CreateView):
    model = Review
    form_class = RateCarUserForm
    template_name = "rate_car.html"

    def post(self, request, id):
        form = self.form_class(request.POST)
        # import pdb;pdb.set_trace()
        if form.is_valid():
            review = form.save(commit=False)
            car = Car.objects.get(id=id)
            review.user = request.user
            review.car = car
            review.save()

            messages.success(request, 'Comentário feito com sucesso!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/add_new_car')

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class DeleteCarView(generic.DeleteView):
    model = Car
    success_url = "/"
