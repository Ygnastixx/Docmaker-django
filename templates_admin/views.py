import json

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GeneratedDocument
from .services.template_prefill_engine import TemplatePrefillEngine
from .services.template_resolver import TemplateResolver
from .services.templating_engine import TemplatingEngine


class DocumentPrefillAPIView(APIView):
    def get(self, request):
        business_code = request.query_params.get("business_code")
        if not business_code:
            return Response({"error": "business_code required"}, status=400)
        params = dict(request.query_params)
        params.pop("business_code", None)
        try:
            template = TemplateResolver().resolve_template(business_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        engine = TemplatePrefillEngine(template)
        data = engine.prefill(params=params)
        return Response(data)


class RenderTemplateAPIView(APIView):
    def post(self, request):
        business_code = request.data.get("business_code")
        if not business_code:
            return Response({"error": "business_code required"}, status=400)
        context = request.data.get("context")

        try:
            template = TemplateResolver().resolve_template(business_code)
        except ValueError as e:
            return Response({"error": str(e)}, status=404)
        engine = TemplatingEngine()
        file_path = engine.render(template.docx_file, context)
        generated = GeneratedDocument(template=template, context_json=context)
        with open(file_path, "rb") as f:
            generated.output_file.save(f"doc_{template.slug}_{generated.id}.docx", f)
        generated.save()
        return Response({"document_id": generated.id, "download_url": generated.output_file.url})

