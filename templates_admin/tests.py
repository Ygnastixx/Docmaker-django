from django.test import TestCase
from unittest.mock import patch
from .models import TemplateDocument, TemplateField, DatasourceRegistry, DocumentType
from .services.template_prefill_engine import TemplatePrefillEngine
from .services.template_resolver import TemplateResolver
from .services.templating_engine import TemplatingEngine
import os


class PrefillAndResolverTests(TestCase):
    @patch("templates_admin.services.datasource_engine.requests.get")
    def test_prefill_and_resolve(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"username": "John Doe"}
        ds = DatasourceRegistry.objects.create(name="Users", api_endpoint="http://example/api/user/1")
        tpl = TemplateDocument.objects.create(name="T", slug="t1", docx_file="tests/sample.docx")
        f = TemplateField.objects.create(document=tpl, name="username", field_type="text",
                                         datasource=ds, datasource_key="username", is_user_input=False)
        DocumentType.objects.create(code="test_code", template=tpl)
        # resolve via business code
        resolved = TemplateResolver().resolve_template("test_code")
        self.assertEqual(resolved, tpl)
        engine = TemplatePrefillEngine(tpl)
        data = engine.prefill(params={})
        self.assertEqual(data["fields"][0]["value"], "John Doe")


class RenderEngineTests(TestCase):
    def test_render(self):
        tpl = TemplateDocument.objects.create(name="T2", slug="t2", docx_file="tests/sample.docx")
        engine = TemplatingEngine()
        context = {"name": "John"}
        fp = engine.render(tpl.docx_file, context)
        self.assertTrue(os.path.exists(fp))
