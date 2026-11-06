from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Count, Sum

from .forms import RegisterForm, ProfileUpdateForm, AdminUserUpdateForm
from orders.models import Order


# ==============================================================================
# AUTHENTIFICATION & COMPTE CLIENT
# ==============================================================================

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Bienvenue {user.first_name} ! Votre compte a été créé avec succès.")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('home')


@login_required
def dashboard_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Vos coordonnées ont été mises à jour.")
            return redirect('accounts:dashboard')
    else:
        form = ProfileUpdateForm(instance=profile)

    # Si l'utilisateur est Staff/Administrateur : il voit tous les tirages de tous les clients
    if request.user.is_staff:
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Client normal : il ne voit QUE ses propres tirages
        orders = Order.objects.filter(
            client_email=request.user.email
        ).order_by('-created_at')

        if not orders.exists():
            orders = Order.objects.filter(
                client_name=request.user.get_full_name() or request.user.username
            ).order_by('-created_at')

    return render(request, 'accounts/dashboard.html', {
        'form': form,
        'orders': orders
    })


# ==============================================================================
# GESTION UTILISATEURS (ACCÈS STAFF / ADMIN)
# ==============================================================================

@staff_member_required
def admin_user_list_view(request):
    """Liste avec recherche et filtres par statut / rôle."""
    users = User.objects.select_related('profile').annotate(
        orders_count=Count('orders'),
        total_spent=Sum('orders__total_ttc')
    ).order_by('-date_joined')

    # Filtrage par recherche
    query = request.GET.get('q', '').strip()
    if query:
        users = users.filter(
            username__icontains=query
        ) | users.filter(
            email__icontains=query
        ) | users.filter(
            first_name__icontains=query
        ) | users.filter(
            last_name__icontains=query
        ) | users.filter(
            profile__company_name__icontains=query
        )

    # Filtrage par rôle
    role = request.GET.get('role')
    if role == 'staff':
        users = users.filter(is_staff=True)
    elif role == 'clients':
        users = users.filter(is_staff=False)

    return render(request, 'accounts/admin_user_list.html', {
        'users_list': users,
        'query': query,
        'selected_role': role
    })


@staff_member_required
def admin_user_detail_view(request, user_id):
    """Fiche détaillée d'un utilisateur et historique complet de ses commandes."""
    target_user = get_object_or_404(User.objects.select_related('profile'), id=user_id)
    
    # Récupération des commandes du client
    orders = Order.objects.filter(
        client_email=target_user.email
    ).order_by('-created_at')

    if not orders.exists():
        orders = Order.objects.filter(
            client_name=target_user.get_full_name() or target_user.username
        ).order_by('-created_at')

    return render(request, 'accounts/admin_user_detail.html', {
        'target_user': target_user,
        'orders': orders
    })


@staff_member_required
def admin_user_edit_view(request, user_id):
    """Édition personnalisée d'un utilisateur et de son profil."""
    target_user = get_object_or_404(User.objects.select_related('profile'), id=user_id)

    if request.method == 'POST':
        form = AdminUserUpdateForm(request.POST, instance=target_user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Le compte de {target_user.username} a été mis à jour.")
            return redirect('accounts:admin_user_detail', user_id=target_user.id)
    else:
        form = AdminUserUpdateForm(instance=target_user)

    return render(request, 'accounts/admin_user_edit.html', {
        'target_user': target_user,
        'form': form
    })


@staff_member_required
def admin_user_toggle_status_view(request, user_id):
    """Active ou désactive un utilisateur en un clic."""
    target_user = get_object_or_404(User, id=user_id)
    if target_user == request.user:
        messages.error(request, "Vous ne pouvez pas désactiver votre propre compte administrateur.")
    else:
        target_user.is_active = not target_user.is_active
        target_user.save()
        status_label = "activé" if target_user.is_active else "désactivé"
        messages.info(request, f"Le compte de {target_user.username} a été {status_label}.")
    
    return redirect(request.META.get('HTTP_REFERER', 'accounts:admin_user_list'))