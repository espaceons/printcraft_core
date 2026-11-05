# orders/models.py
from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Brouillon / Devis'),
        ('SUBMITTED', 'Commande validée'),
        ('PREFLIGHT_OK', 'Fichier validé pour tirage'),
        ('PRINTING', 'En cours d\'impression'),
        ('COMPLETED', 'Terminée et livrée'),
    ]
    PRODUCT_TYPES = [
        ('BOOK', 'Livre'),
        ('SHEET', 'Feuille simple / Affiche'),
        ('ENVELOPE', 'Enveloppe'),
    ]

    client_name = models.CharField(max_length=150)
    client_email = models.EmailField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    quantity = models.PositiveIntegerField(default=50)
    
    # Paramètres techniques au moment de la commande
    specs_json = models.JSONField(help_text="Stocke les choix: format, grammage, reliure...")
    
    total_ht = models.DecimalField(max_digits=8, decimal_places=2)
    total_ttc = models.DecimalField(max_digits=8, decimal_places=2)
    
    pdf_file = models.FileField(upload_to='customer_files/%Y/%m/', null=True, blank=True)
    detected_pages = models.PositiveIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.client_name} ({self.get_product_type_display()})"