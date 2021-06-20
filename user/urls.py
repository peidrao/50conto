from django.urls import path

from . import views

urlpatterns = [
    # path('register/', views.register, name='register'),
    path('register/', views.SignUpUser.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    # path('login/', views.login, name='login')
]