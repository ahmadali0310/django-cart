from django.urls import  path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("cart/", views.cart, name="cart"),
    path("update_cart/", views.update_cart, name="update_cart"),
]