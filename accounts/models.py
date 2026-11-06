from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    CLIENT_TYPES = [
        ('INDIVIDUAL', 'Particulier / Auteur'),
        ('COMPANY', 'Entreprise / Éditeur'),
        ('AGENCY', 'Agence / Graphiste'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPES, default='INDIVIDUAL')
    company_name = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nom de l'entreprise")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    address = models.TextField(blank=True, null=True, verbose_name="Adresse de livraison")
    vat_number = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de TVA (optionnel)")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profil de {self.user.username} ({self.get_client_type_display()})"

# Signal pour créer ou mettre à jour automatiquement le profil lors de la création d'un User
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()