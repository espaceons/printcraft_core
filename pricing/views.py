# pricing/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal
from catalog.models import PaperWeight, BindingType
from .services import PrintPriceCalculator

class CalculateQuoteAPIView(APIView):
    def post(self, request):
        data = request.data
        product_type = data.get("product_type", "BOOK")
        quantity = int(data.get("quantity", 50))

        if product_type == "BOOK":
            pages = int(data.get("pages", 120))
            is_color = bool(data.get("is_color", False))
            lamination = bool(data.get("lamination", True))
            
            weight_id = data.get("paper_weight_id")
            binding_code = data.get("binding_code", "PUR")

            try:
                paper_weight = PaperWeight.objects.get(id=weight_id) if weight_id else PaperWeight.objects.first()
                binding = BindingType.objects.get(code=binding_code)
            except (PaperWeight.DoesNotExist, BindingType.DoesNotExist):
                return Response({"error": "Configuration technique introuvable"}, status=status.HTTP_400_BAD_REQUEST)

            spine_mm = PrintPriceCalculator.calculate_spine_thickness(
                pages, paper_weight.thickness_per_sheet_mm
            )

            quote = PrintPriceCalculator.calculate_book_quote(
                pages=pages,
                quantity=quantity,
                paper_cost_sheet=paper_weight.cost_per_sheet_a4,
                is_color=is_color,
                binding_setup=binding.base_setup_cost,
                binding_unit=binding.unit_cost,
                lamination=lamination
            )
            quote["spine_thickness_mm"] = spine_mm
            return Response(quote, status=status.HTTP_200_OK)

        return Response({"error": "Type de produit non pris en charge pour l'instant"}, status=status.HTTP_400_BAD_REQUEST)