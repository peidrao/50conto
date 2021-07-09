from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'user'

urlpatterns = [
    path('register/', views.SignUpUserView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
    path('lessee/<str:pk>', views.LesseeProfile.as_view(), name='lessee'),
    path('profile/', login_required(views.ProfileUserView.as_view()), name='profile'),
    path('add_new_car/', login_required(views.UserCreateCarView.as_view()), name='add_new_car'),
    path('list_cars/<int:pk>', login_required(views.ListUserCarsView.as_view()), name='list_cars'),
    path('update_car/<int:pk>', login_required(views.UpdateCarView.as_view()), name='update_car'),
    path('delete_car/<int:pk>', login_required(views.DeleteCarView.as_view()), name='delete_car'),
    path('my_car/<int:pk>', login_required(views.ListMyCarView.as_view()), name='my_car'),
    path('rate_car/<int:id>', login_required(views.RateCarUserView.as_view()), name='rate_car'),
]