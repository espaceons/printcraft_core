# orders/urls.py
from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('new/', views.create_order_view, name='order_create'),
    path('reprint/<int:pk>/', views.reprint_order_view, name='order_reprint'),
]
