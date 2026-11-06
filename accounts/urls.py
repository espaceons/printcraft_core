from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Espace Authentification & Dashboard Client
    path('register/', views.register_view, name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Espace Gestion Utilisateurs (Staff / Admin)
    path('manage/users/', views.admin_user_list_view, name='admin_user_list'),
    path('manage/users/<int:user_id>/', views.admin_user_detail_view, name='admin_user_detail'),
    path('manage/users/<int:user_id>/edit/', views.admin_user_edit_view, name='admin_user_edit'),
    path('manage/users/<int:user_id>/toggle/', views.admin_user_toggle_status_view, name='admin_user_toggle'),
]