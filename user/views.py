from pdb import set_trace
from django.contrib.auth import authenticate, login as auth_login, logout as logout_func
from django.shortcuts import get_object_or_404, render, HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic.base import TemplateView
# Create your views here.

from django.views.generic.edit import CreateView, DeleteView, ModelFormMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View, ListView, UpdateView
from django.urls import reverse_lazy

from user.forms import RegisterUserForm
from car.forms import RegisterCarForm, CarUpdateForm
from user.models import User
from car.models import Car

class LoginView(View):
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
        

class SignUpUserView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'register_user.html'
    success_url =  reverse_lazy('index')
    form_class = RegisterUserForm
    success_message = 'Usuário cadastrado com sucesso'


class LogoutUserView(View):
    def get(self, request):
        logout_func(request)
        return HttpResponseRedirect('/')


class ProfileUserView(TemplateView):
    model = User
    template_name = 'profile_user.html'


class UserCreateCarView(SuccessMessageMixin, CreateView):
    template_name = 'register_car.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request):
        form = RegisterCarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.user = request.user
            car.save()
            # data = Car()
            # import pdb;pdb.set_trace()
            
            # data.save()
            messages.success(request, 'Carro adicionado a sua conta')
            return HttpResponseRedirect('/add_new_car')
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect('/add_new_car')


class ListUserCarsView(ListView):
    template_name = 'list_cars.html'

    def get_queryset(self):
        pk = self.kwargs['pk']
        user = Car.objects.filter(user_id=pk)
        return user

class UpdateCarView(UpdateView):
    model = Car
    template_name = "update_car.html"
    context_object_name = 'car_update'
    success_message = 'Carro editado com sucesso'
    success_url = "/"
    form_class = CarUpdateForm

    def form_invalid(self, form):
        return HttpResponse("form is invalid.. this is just an HttpResponse object")


class DeleteCarView(DeleteView):
    model = Car
    success_url ="/"
    



        

# # form = RegisterCarForm(request.POST, request.FILES)
#         if form.is_valid():
#             car = form.save(commit=False)
#             car.user = request.user
#             car.save()
#             # data = Car()
#             # import pdb;pdb.set_trace()
            
#             # data.save()
#             messages.success(request, 'Carro adicionado a sua conta')
#             return HttpResponseRedirect('/add_new_car')
#         else:
#             messages.warning(request, form.errors)
#             return HttpResponseRedirect('/add_new_car')


    # def post(self, request, *args, **kwargs):
    #     # Get instance of PhysicalPart
    #     self.object = self.get_object()
    #     # Load form
    #     form = self.get_form()
    #     # Add choices to form 'subcategory' field
    #     form.fields['subcategory'].choices = SubcategoryFilter[self.object.category]
    #     # Check if form is valid and save PhysicalPart instance
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
            # return self.form_invalid(form)