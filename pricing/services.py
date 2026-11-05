# pricing/services.py
from decimal import Decimal
import math

class PrintPriceCalculator:

    @staticmethod
    def calculate_spine_thickness(page_count: int, thickness_per_sheet: float) -> float:
        """Calcule l'épaisseur de la tranche en mm."""
        sheets = math.ceil(page_count / 2)
        # Épaisseur = feuilles intérieures + ~0.5mm pour le carton/rainage de couverture
        spine = (sheets * thickness_per_sheet) + 0.5
        return round(spine, 2)

    @classmethod
    def calculate_book_quote(cls, pages: int, quantity: int, paper_cost_sheet: Decimal, 
                             is_color: bool, binding_setup: Decimal, binding_unit: Decimal,
                             lamination: bool = True) -> dict:
        sheets_per_book = math.ceil(pages / 2)
        
        # 1. Coût impression page (N&B vs Couleur)
        print_cost_per_sheet = Decimal('0.07') if is_color else Decimal('0.015')
        inner_cost_per_book = sheets_per_book * (paper_cost_sheet + print_cost_per_sheet)

        # 2. Couverture (papier 300g couché + impression couleur)
        cover_cost = Decimal('0.45')
        if lamination:
            cover_cost += Decimal('0.25') # Pelliculage mat/brillant

        # 3. Reliure
        total_binding = binding_setup + (binding_unit * quantity)

        # 4. Total brut de production
        production_total = (inner_cost_per_book + cover_cost) * quantity + total_binding

        # 5. Barème de remise sur volume
        discount = Decimal('0.00')
        if quantity >= 200:
            discount = Decimal('0.20')
        elif quantity >= 100:
            discount = Decimal('0.15')
        elif quantity >= 50:
            discount = Decimal('0.10')

        total_ht = production_total * (Decimal('1.00') - discount)
        unit_ht = total_ht / quantity
        
        # TVA réduite pour les livres (5.5%)
        tax_rate = Decimal('0.055')
        total_ttc = total_ht * (Decimal('1.00') + tax_rate)

        return {
            "quantity": quantity,
            "unit_price_ht": round(unit_ht, 2),
            "total_ht": round(total_ht, 2),
            "tva": round(total_ht * tax_rate, 2),
            "total_ttc": round(total_ttc, 2),
            "discount_applied_percent": int(discount * 100)
        }