from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from printcraft_core.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', home_view, name='home'),
    path('pricing/', include('pricing.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)