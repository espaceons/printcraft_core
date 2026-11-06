# orders/forms.py
from django import forms
from .models import Order
from catalog.models import PaperWeight, BindingType

FORMAT_CHOICES = [
    ('A5', 'A5 (148 x 210 mm) - Idéal Roman & Livre'),
    ('A4', 'A4 (210 x 297 mm) - Thèse, Rapport, Magazine'),
    ('A3', 'A3 (297 x 420 mm) - Grand format, Affiche'),
]

COLOR_CHOICES = [
    ('BW', 'Noir & Blanc (Texte seul)'),
    ('COLOR', 'Couleur intégrale (Illustrations, photos)'),
]

class OrderCreateForm(forms.ModelForm):
    page_format = forms.ChoiceField(
        choices=FORMAT_CHOICES, 
        initial='A5', 
        label="Format du document",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    paper_choice = forms.ModelChoiceField(
        queryset=PaperWeight.objects.select_related('paper_type').all(),
        label="Papier & Grammage intérieur",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    binding_choice = forms.ModelChoiceField(
        queryset=BindingType.objects.all(),
        label="Mode de reliure",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    print_color = forms.ChoiceField(
        choices=COLOR_CHOICES,
        label="Type d'impression intérieure",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Order
        fields = ['product_type', 'quantity', 'pdf_file']
        widgets = {
            'product_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf'}),
        }