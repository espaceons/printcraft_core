from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Prénom")
    last_name = forms.CharField(max_length=30, required=True, label="Nom")
    email = forms.EmailField(required=True, label="Adresse e-mail")
    client_type = forms.ChoiceField(choices=UserProfile.CLIENT_TYPES, label="Vous êtes")
    company_name = forms.CharField(max_length=150, required=False, label="Nom de l'entreprise")
    phone = forms.CharField(max_length=20, required=True, label="Numéro de téléphone")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'client_type', 'company_name', 'phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.profile
            profile.client_type = self.cleaned_data['client_type']
            profile.company_name = self.cleaned_data['company_name']
            profile.phone = self.cleaned_data['phone']
            profile.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['client_type', 'company_name', 'phone', 'address', 'vat_number']
        widgets = {
            'client_type': forms.Select(attrs={'class': 'form-select'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vat_number': forms.TextInput(attrs={'class': 'form-control'}),
        }


class AdminUserUpdateForm(forms.ModelForm):
    """Formulaire d'administration personnalisée pour modifier un compte utilisateur et son profil."""
    first_name = forms.CharField(
        max_length=30, 
        required=False, 
        label="Prénom", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False, 
        label="Nom", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        label="Adresse e-mail", 
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    is_active = forms.BooleanField(
        required=False, 
        label="Compte actif", 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    is_staff = forms.BooleanField(
        required=False, 
        label="Accès Staff / Atelier", 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    # Données du profil rattaché
    client_type = forms.ChoiceField(
        choices=UserProfile.CLIENT_TYPES, 
        label="Type de client", 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    company_name = forms.CharField(
        max_length=150, 
        required=False, 
        label="Nom de l'entreprise", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20, 
        required=False, 
        label="Numéro de téléphone", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    vat_number = forms.CharField(
        max_length=50, 
        required=False, 
        label="Numéro de TVA", 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        required=False, 
        label="Adresse de livraison / facturation", 
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'is_active', 'is_staff']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pré-remplissage des champs du profil lors de l'ouverture du formulaire
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['client_type'].initial = profile.client_type
            self.fields['company_name'].initial = profile.company_name
            self.fields['phone'].initial = profile.phone
            self.fields['vat_number'].initial = profile.vat_number
            self.fields['address'].initial = profile.address

    def save(self, commit=True):
        user = super().save(commit=commit)
        if hasattr(user, 'profile'):
            profile = user.profile
            profile.client_type = self.cleaned_data['client_type']
            profile.company_name = self.cleaned_data['company_name']
            profile.phone = self.cleaned_data['phone']
            profile.vat_number = self.cleaned_data['vat_number']
            profile.address = self.cleaned_data['address']
            if commit:
                profile.save()
        return user