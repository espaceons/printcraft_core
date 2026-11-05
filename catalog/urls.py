# catalog/urls.py
from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    # Types de papier
    path('papers/', views.PaperTypeListView.as_view(), name='papertype_list'),
    path('papers/create/', views.PaperTypeCreateView.as_view(), name='papertype_create'),
    path('papers/<int:pk>/edit/', views.PaperTypeUpdateView.as_view(), name='papertype_update'),
    path('papers/<int:pk>/delete/', views.PaperTypeDeleteView.as_view(), name='papertype_delete'),

    # Grammages
    path('weights/', views.PaperWeightListView.as_view(), name='paperweight_list'),
    path('weights/create/', views.PaperWeightCreateView.as_view(), name='paperweight_create'),
    path('weights/<int:pk>/edit/', views.PaperWeightUpdateView.as_view(), name='paperweight_update'),
    path('weights/<int:pk>/delete/', views.PaperWeightDeleteView.as_view(), name='paperweight_delete'),

    # Reliures
    path('bindings/', views.BindingTypeListView.as_view(), name='bindingtype_list'),
    path('bindings/create/', views.BindingTypeCreateView.as_view(), name='bindingtype_create'),
    path('bindings/<int:pk>/edit/', views.BindingTypeUpdateView.as_view(), name='bindingtype_update'),
    path('bindings/<int:pk>/delete/', views.BindingTypeDeleteView.as_view(), name='bindingtype_delete'),
]