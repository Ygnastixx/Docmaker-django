
import os
from tempfile import NamedTemporaryFile
from docxtpl import DocxTemplate
from django.conf import settings


class TemplatingEngine:
    def render(self, template_file, context: dict) -> str:
        """
        template_file = fichier de template
        context = dict Python pour remplir le template
        """
        if not template_file:
            raise ValueError("Template file non défini")
        template_path = template_file.name

        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template introuvable: {template_path}")

        doc = DocxTemplate(template_path)
        doc.render(context)

        # chemin vers /templates_admin/generated_docs
        tmp = NamedTemporaryFile(delete=False, suffix=".docx", dir=settings.TEMPLATES_ADMIN_GENERATED_DOCS_DIR)
        doc.save(tmp.name)
        tmp.close()
        return tmp.name
