from django.contrib import admin
from .models import TemplateDocument, TemplateField, DatasourceRegistry, FieldDatasourceMapping, DocumentType


class FieldDatasourceMappingInline(admin.TabularInline):
    model = FieldDatasourceMapping
    extra = 1


class TemplateFieldInline(admin.TabularInline):
    model = TemplateField
    extra = 1
    fields = ('name', 'label', 'field_type', 'datasource', 'datasource_key', 'options', 'order', 'required',
              'is_multiple', 'is_user_input')


@admin.register(TemplateDocument)
class TemplateDocumentAdmin(admin.ModelAdmin):
    inlines = [TemplateFieldInline]
    list_display = ('name', 'slug')


@admin.register(DatasourceRegistry)
class DatasourceRegistryAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_endpoint')


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "description", "template", "is_active")
