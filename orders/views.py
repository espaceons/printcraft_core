# orders/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from .forms import OrderCreateForm
from files_manager.services import PreflightChecker
from pricing.services import PrintPriceCalculator
from catalog.models import PaperWeight, BindingType
from decimal import Decimal
from django.db import transaction


@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderCreateForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)

                    # 1. Rattachement au compte utilisateur
                    if hasattr(order, 'user'):
                        order.user = request.user

                    order.client_name = request.user.get_full_name() or request.user.username
                    order.client_email = request.user.email or f"{request.user.username}@myprint.local"

                    # 2. Contrôle prépresse automatique si un fichier PDF est envoyé
                    pdf = request.FILES.get('pdf_file')
                    detected_pages = 50  # Valeur de secours si aucun PDF

                    if pdf:
                        try:
                            pdf_info = PreflightChecker.inspect_pdf(pdf)
                            detected_pages = pdf_info['pages']
                            order.detected_pages = detected_pages
                            order.status = 'PREFLIGHT_OK'
                        except Exception as e:
                            messages.error(
                                request, f"Erreur de prépresse : {e}")
                            return render(request, 'orders/order_create.html', {'form': form})

                    # 3. Récupération des choix dynamiques du formulaire
                    page_format = form.cleaned_data.get('page_format', 'A5')
                    paper_choice = form.cleaned_data.get('paper_choice')
                    binding_choice = form.cleaned_data.get('binding_choice')
                    print_color = form.cleaned_data.get('print_color', 'BW')
                    is_color = (print_color == 'COLOR')

                    # Valeurs de secours si les champs n'existent pas encore dans le formulaire
                    if not paper_choice:
                        paper_choice = PaperWeight.objects.select_related('paper_type').first()
                    if not binding_choice:
                        binding_choice = BindingType.objects.filter(code='PUR').first()

                    # Coefficient de surface de papier selon le format choisi :
                    # A4 = référence (1.0) | A3 = double surface (2.0) | A5 = demi-surface (0.50)
                    format_multiplier = Decimal('1.0')
                    if page_format == 'A3':
                        format_multiplier = Decimal('2.0')
                    elif page_format == 'A5':
                        format_multiplier = Decimal('0.55')  # Légère marge technique de calage/chutes

                    base_sheet_cost = paper_choice.cost_per_sheet_a4 if paper_choice else Decimal('0.015')
                    adjusted_paper_cost = base_sheet_cost * format_multiplier

                    # 4. Calcul de l'épaisseur du dos (tranche en mm) pour les livres
                    sheet_thickness = paper_choice.thickness_per_sheet_mm if paper_choice else 0.10
                    spine_mm = PrintPriceCalculator.calculate_spine_thickness(
                        detected_pages, 
                        sheet_thickness
                    )

                    # 5. Enregistrement des spécifications techniques détaillées
                    order.specs_json = {
                        "format": page_format,
                        "pages": detected_pages,
                        "paper": str(paper_choice) if paper_choice else "Standard 80g",
                        "binding": binding_choice.name if binding_choice else "Dos Carré Collé",
                        "color": "Couleur" if is_color else "Noir & Blanc",
                        "spine_thickness_mm": spine_mm,
                    }

                    # 6. Moteur de calcul du devis
                    binding_setup = binding_choice.base_setup_cost if binding_choice else Decimal('15.00')
                    binding_unit = binding_choice.unit_cost if binding_choice else Decimal('1.20')

                    quote = PrintPriceCalculator.calculate_book_quote(
                        pages=detected_pages,
                        quantity=order.quantity,
                        paper_cost_sheet=adjusted_paper_cost,
                        is_color=is_color,
                        binding_setup=binding_setup,
                        binding_unit=binding_unit,
                    )

                    order.total_ht = quote['total_ht']
                    order.total_ttc = quote['total_ttc']
                    order.save()

                    messages.success(
                        request,
                        f"Tirage #{order.id} validé ! "
                        f"Format {page_format}, {detected_pages} pages, dos estimé à {spine_mm} mm."
                    )
                    return redirect('accounts:dashboard')

            except Exception as e:
                messages.error(request, f"Une erreur est survenue lors de l'enregistrement : {e}")
                return render(request, 'orders/order_create.html', {'form': form})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order_create.html', {'form': form})


@login_required
def reprint_order_view(request, pk):
    """Réimprime une commande existante en dupliquant ses paramètres techniques."""
    past_order = get_object_or_404(Order, pk=pk)

    # Nouvelle instance clonant les spécifications techniques et le fichier PDF existant
    new_order = Order.objects.create(
        client_name=past_order.client_name,
        client_email=past_order.client_email,
        product_type=past_order.product_type,
        quantity=past_order.quantity,
        specs_json=past_order.specs_json,
        total_ht=past_order.total_ht,
        total_ttc=past_order.total_ttc,
        pdf_file=past_order.pdf_file,
        detected_pages=past_order.detected_pages,
        status='PREFLIGHT_OK'
    )

    messages.success(
        request, f"Réimpression lancée ! Commande #{new_order.id} créée à partir du tirage #{past_order.id}.")
    return redirect('accounts:dashboard')
