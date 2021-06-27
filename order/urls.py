from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'order'

urlpatterns = [
    path('add_shopcart/<int:id>', login_required(views.AddCartInShopCartView.as_view()), name='add_shopcart'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/<int:pk>', views.DeleteCartView.as_view(), name='delete_cart'),
    path('order/', views.CreateOrderView.as_view(), name='create_order')
]