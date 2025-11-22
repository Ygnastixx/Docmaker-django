from django.urls import path
from .views import DocumentPrefillAPIView, RenderTemplateAPIView

urlpatterns = [
    path("prefill/", DocumentPrefillAPIView.as_view(), name="doc-prefill"),
    path("render/", RenderTemplateAPIView.as_view(), name="doc-render"),
]
