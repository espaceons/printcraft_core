# pricing/urls.py
from django.urls import path
from .views import CalculateQuoteAPIView

urlpatterns = [
    path('api/quote/', CalculateQuoteAPIView.as_view(), name='api-quote'),
]