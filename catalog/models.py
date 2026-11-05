# catalog/models.py
from django.db import models

class PaperType(models.Model):
    name = models.CharField(max_length=100) # ex: Bouffant, Offset, Couché Satiné
    bulk_factor = models.DecimalField(
        max_digits=4, decimal_places=2, default=1.0, 
        help_text="Main du papier (ex: 1.8 pour bouffant, 1.0 pour couché)"
    )

    def __str__(self):
        return self.name

class PaperWeight(models.Model):
    paper_type = models.ForeignKey(PaperType, on_delete=models.CASCADE, related_name="weights")
    grammage = models.PositiveIntegerField(help_text="en g/m² (ex: 80, 115, 300)")
    cost_per_sheet_a4 = models.DecimalField(max_digits=6, decimal_places=4, help_text="Coût brut par feuille A4")

    def __str__(self):
        return f"{self.paper_type.name} {self.grammage}g"

    @property
    def thickness_per_sheet_mm(self):
        # Épaisseur théorique en mm = (Grammage / 1000) * Main
        return (float(self.grammage) / 1000.0) * float(self.paper_type.bulk_factor)

class BindingType(models.Model):
    CODE_CHOICES = [
        ('PUR', 'Dos Carré Collé PUR'),
        ('WIRO', 'Spirale Métallique (Wire-O)'),
        ('STITCH', '2 Agrafes (Piqûre à cheval)'),
    ]
    code = models.CharField(max_length=10, choices=CODE_CHOICES, unique=True)
    name = models.CharField(max_length=100)
    base_setup_cost = models.DecimalField(max_digits=6, decimal_places=2, default=15.00)
    unit_cost = models.DecimalField(max_digits=6, decimal_places=2, default=1.20)
    min_pages = models.PositiveIntegerField(default=4)
    max_pages = models.PositiveIntegerField(default=800)

    def __str__(self):
        return self.name