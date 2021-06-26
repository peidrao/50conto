from django.urls import path

from . import views

app_name = 'car'

urlpatterns = [
    path('car_detail/<int:pk>', views.CarDetailView.as_view(), name='car_detail'),
]