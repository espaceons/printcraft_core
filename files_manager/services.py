# files_manager/services.py
from pypdf import PdfReader
from django.core.exceptions import ValidationError

class PreflightChecker:
    @staticmethod
    def inspect_pdf(file_path_or_buffer):
        try:
            reader = PdfReader(file_path_or_buffer)
            page_count = len(reader.pages)
            if page_count == 0:
                raise ValidationError("Le fichier PDF est vide.")
            
            first_page = reader.pages[0]
            width_pt = float(first_page.mediabox.width)
            height_pt = float(first_page.mediabox.height)

            # Conversion points Typo en millimètres (1 pt = 0.352778 mm)
            width_mm = round(width_pt * 0.352778, 1)
            height_mm = round(height_pt * 0.352778, 1)

            return {
                "pages": page_count,
                "width_mm": width_mm,
                "height_mm": height_mm
            }
        except Exception as e:
            raise ValidationError(f"Erreur lors de l'analyse du PDF : {str(e)}")