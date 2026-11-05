# catalog/forms.py
from django import forms
from .models import PaperType, PaperWeight, BindingType

class PaperTypeForm(forms.ModelForm):
    class Meta:
        model = PaperType
        fields = ['name', 'bulk_factor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Bouffant, Couché...'}),
            'bulk_factor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'name': 'Nom du papier',
            'bulk_factor': 'Main du papier (ex: 1.8)',
        }

class PaperWeightForm(forms.ModelForm):
    class Meta:
        model = PaperWeight
        fields = ['paper_type', 'grammage', 'cost_per_sheet_a4']
        widgets = {
            'paper_type': forms.Select(attrs={'class': 'form-select'}),
            'grammage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 80, 115, 300'}),
            'cost_per_sheet_a4': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0001'}),
        }
        labels = {
            'paper_type': 'Type de papier associé',
            'grammage': 'Grammage (g/m²)',
            'cost_per_sheet_a4': 'Coût brut par feuille A4 (€)',
        }

class BindingTypeForm(forms.ModelForm):
    class Meta:
        model = BindingType
        fields = ['code', 'name', 'base_setup_cost', 'unit_cost', 'min_pages', 'max_pages']
        widgets = {
            'code': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'base_setup_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'min_pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_pages': forms.NumberInput(attrs={'class': 'form-control'}),
        }