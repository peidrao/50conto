from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as logout_func
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.http.response import BadHeaderError
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy as _
from django.views import generic

from api import settings
from car.forms import RateCarUserForm, RegisterCarForm, UpdateCarForm
from car.models import Car, Review
from order.models import Order
from user.forms import RegisterUserForm
from user.models import User
from user.service import CreateView as CreateViewUser


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


class SignUpUserView(SuccessMessageMixin, CreateViewUser):
    model = User
    template_name = 'register_user.html'
    success_url = _('user:register')
    form_class = RegisterUserForm
    success_message = 'Usuário cadastrado com sucesso'

    def form_invalid(self, form):
        messages.error(self.request, form.error_messages)
        return HttpResponseRedirect(_('user:register'))

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
        form = RegisterCarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()

            messages.success(request, 'Carro adicionado a sua conta')
            return HttpResponseRedirect('/add_new_car')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/add_new_car')


class ListUserCarsView(generic.ListView):
    template_name = 'list_cars.html'

    def get(self, request, *args, **kwargs):
        car = Car.objects.filter(user_id=self.kwargs['pk'])
        context = {'car_list': car}

        return render(request, self.template_name, context)


class ListMyCarView(generic.ListView):
    template_name = 'my_car.html'
    context_object_name = "my_car"

    def get(self, request, *args, **kwargs):
        order_car = Order.objects.filter(user_id=request.user.id)
        return render(request, self.template_name, {'order_car': order_car})

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = Car.objects.filter(user_id=pk)
        return user


class UpdateCarView(generic.UpdateView):
    template_name = "update_car.html"
    model = Car
    form_class = UpdateCarForm
    success_message = 'Carro editado com sucesso'
    success_url = "/"

    def get(self, request, *args, **kwargs):
        car = Car.objects.get(id=kwargs['pk'])
        context = {
            'car_update': car,
            'car_options': Car
        }
        return render(request, self.template_name, context)


class RateCarUserView(generic.CreateView):
    model = Review
    form_class = RateCarUserForm
    template_name = "rate_car.html"

    def post(self, request, id):
        form = self.form_class(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            order = Order.objects.get(id=self.kwargs['id'])
            review.order = order
            review.user = request.user
            review.car = order.car
            review.save()

            messages.success(request, 'Comentário feito com sucesso!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/add_new_car')


class DeleteCarView(generic.DeleteView):
    model = Car
    success_url = "/"


class LesseeProfile(generic.CreateView):
    template_name = 'lesse_profile.html'

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['pk'])
        cars = Car.objects.filter(user_id=user.id)
        context = {
            'user': user,
            'cars': cars
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('email', '')
        if subject and message and from_email:
            try:
                send_mail(subject, message, from_email, [settings.EMAIL_HOST_USER])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return HttpResponseRedirect('/contact/thanks/')
        else:
            return HttpResponse('Make sure all fields are entered and valid.')
