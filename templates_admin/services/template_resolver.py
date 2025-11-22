from django.core.exceptions import ObjectDoesNotExist
from ..models import DocumentType


class TemplateResolver:
    def resolve_template(self, business_code: str):
        try:
            entry = DocumentType.objects.get(code=business_code, is_active=True)
            return entry.template
        except ObjectDoesNotExist:
            raise ValueError(f"No template for business_code '{business_code}'")
