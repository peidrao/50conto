from django.contrib.auth import authenticate, login as auth_login, logout as logout_func
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import View
from django.urls import reverse_lazy

from user.forms import RegisterUserForm
from user.models import User


# def login(request):
#     if request.method == 'POST':
#         email = request.POST['email']
#         password = request.POST['password']
#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             auth_login(request, user)
#             # current_user = request.user
#             # userprofile = User.objects.get(user_id=current_user.id)
#             # request.session['userimage'] = userprofile.image.url
#             return HttpResponseRedirect('/profile')
#         else:
#             messages.warning(
#                 request, 'Erro! Lemail ou senha errados')
#             return HttpResponseRedirect('/login')

#     # genre = Genre.objects.all()
#     # context = {'genre': genre}
    # return render(request, 'login_user.html', {})


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
        
    


class SignUpUser(SuccessMessageMixin, CreateView):
    template_name = 'register_user.html'
    success_url =  reverse_lazy('index')
    form_class = RegisterUserForm
    success_message = 'Usuário cadastrado com sucesso'


# def register(request):
#     if request.method == 'POST':
#         form = RegisterUserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=password)
#             auth_login(request, user)
#             current_user = request.user
#             data = User()
#             data.user_id = current_user.id
#             # data.image = 'images/users/user.png'
#             data.save()
#             messages.success(request, 'Sua conta foi criada com sucesso!')
#             return HttpResponseRedirect('/')
#         else:
#             messages.warning(request, form.errors)
#             return HttpResponseRedirect('/register')

#     form = RegisterUserForm()
#     # genre = Genre.objects.all()
#     context = {'form': form}
#     return render(request, 'register_user.html', context)