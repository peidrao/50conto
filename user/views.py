from user.forms import RegisterUserForm
from django.http.response import BadHeaderError
from api import settings
from datetime import datetime
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login as auth_login, logout as logout_func
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.hashers import make_password
from django.contrib import messages

from django.core.exceptions import ValidationError

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.db import connection
from django.views import generic

from car.forms import RateCarUserForm, RegisterCarForm
from user.models import User
from car.models import Car, Review
from order.models import Order


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
    model = User
    template_name = 'register_user.html'
    success_url = reverse_lazy('home:index')
    form_class = RegisterUserForm
    success_message = 'Usuário cadastrado com sucesso'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'user_list': User})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        email = request.POST["email"]
        last_name = request.POST["last_name"]
        type_user = request.POST["type_user"]
        password = request.POST["password1"]
        last_login = datetime.now()
        is_superuser = 0
        is_active = 1
        is_staff = 0
        date_joined = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO user_user VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
                None, make_password(
                    password), last_login, is_superuser, is_staff, is_active, date_joined,
                username, first_name, last_name, 2, type_user, email])

        return HttpResponseRedirect(reverse_lazy('home:index'))


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
        price_day = request.POST["price_day"].replace(',', '.')
        brand = request.POST["brand"]
        image_car = request.POST["image_car"]
        status_car = request.POST["status_car"]
        initial_date = request.POST["initial_date"]
        finish_date = request.POST["finish_date"]
        created_at = datetime.now()
        updated_at = datetime.now()
        user_id = request.user.id

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO car_car VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [
                           None, image_car, brand,  status_car, color, car_model, plaque, price_day, initial_date, finish_date,
                           created_at, updated_at, user_id, ])

            return HttpResponseRedirect(reverse_lazy('user:list_cars', args=[user_id]))


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
        order_car = Order.objects.raw(f'SELECT * from order_shopcart o WHERE EXISTS ( SELECT * FROM order_order WHERE user_id = {request.user.id})')

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
        price_day = request.POST["price_day"].replace(',', '.')
        brand = request.POST["brand"]
        status_car = request.POST["status_car"]
        initial_date = request.POST["initial_date"]
        finish_date = request.POST["finish_date"]
        updated_at = datetime.now()
        user_id = request.user.id
        car_id = self.kwargs['pk']

        with connection.cursor() as cursor:
            cursor.execute("UPDATE car_car \
                            SET updated_at=%s, price_day=%s, brand=%s, plaque=%s, \
                                car_model=%s, color=%s, status_car=%s, initial_date=%s, \
                                finish_date=%s, user_id=%s, image_car=%s \
                                WHERE id = %s", [
                           updated_at, price_day, brand, plaque, car_model, color,
                           status_car, initial_date, finish_date, user_id, image_car, car_id
                           ])

            return HttpResponseRedirect(reverse_lazy('user:profile'))


# TODO: Ver depois que arrumar pedido.
class RateCarUserView(generic.CreateView):
    model = Review
    form_class = RateCarUserForm
    template_name = "rate_car.html"

    def post(self, request, id):
        try:
            order = Order.objects.raw(
                'SELECT * FROM order_order WHERE id = %s', [id])[0]
            car_id = order.car.id
            user_id = request.user.id
            title = request.POST.get('title', '')
            subject = request.POST.get('subject', '')
            comment = request.POST.get('comment', '')
            rate = request.POST.get('rate', '')
            created_at = datetime.now()
            updated_at = datetime.now()

            with connection.cursor() as cursor:
                cursor.execute('INSERT INTO order_review VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)', [
                    None, created_at, updated_at, title, subject, comment, rate, 1, car_id, order.id, user_id
                ])

            messages.success(request, 'Comentário feito com sucesso!')
            return HttpResponseRedirect(reverse_lazy('user:profile'))

        except Exception as error:
            raise ValidationError(error)


class DeleteCarView(generic.DeleteView):
    model = Car
    success_url = "/"

    def post(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM car_car WHERE id= %s", [pk])

        return HttpResponseRedirect(reverse_lazy('user:profile'))


class LesseeProfile(generic.CreateView):
    template_name = 'lesse_profile.html'

    def get(self, request, *args, **kwargs):
        id_username = kwargs['pk']

        user = User.objects.raw(
            'SELECT * FROM user_user WHERE username = %s', [id_username])[0]
        cars = Car.objects.raw(
            'SELECT * FROM car_car where user_id = %s', [user.id])

        context = {
            'user': user,
            'cars': cars
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_username = kwargs['pk']

        user = User.objects.raw(
            'SELECT * FROM user_user WHERE username = %s', [id_username])[0]
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email,
                          [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
