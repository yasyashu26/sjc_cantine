from django.urls import path
from django.contrib.auth.models import User
from inventory.views import home, add_to_cart, remove_from_cart,about, decreaseCart, checkout, CartView, checkout_page, pastorders, products

urlpatterns = [
    path('',home, name='home'),
    path('home/product/<int:pk>/', products, name='products'),
    path('about/', about, name='about'),
    path('cart/<int:pk>/', add_to_cart, name='add-cart'),
    path('remove/<int:pk>/',remove_from_cart, name='remove-cart'),
    path('cart/', CartView,name='cart'),
    path('decrease/<int:pk>/', decreaseCart,name='decrease-cart'),
    path('cart/order_placed/', checkout, name='checkout'),
    path('cart/current_order/', checkout_page,name='checkout_page'),
    path('cart/past_orders',pastorders, name="pastorders" ),
    #path('synccart/', cart_sync, name='cart'),
] 