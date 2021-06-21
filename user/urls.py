from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    # path('register/', views.register, name='register'),
    path('register/', views.SignUpUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='login'),
    path('profile/', login_required(views.ProfileUserView.as_view()), name='profile'),
    # path('login/', views.login, name='login')
]