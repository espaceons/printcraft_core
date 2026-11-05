# pricing/views.py (ou dans une application core/pages)
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')