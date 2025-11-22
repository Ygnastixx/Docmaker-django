import os

from django.db import models
from django.conf import settings


def template_upload_path(instance, filename):
    return os.path.join(str(settings.TEMPLATES_ADMIN_DOC_TEMPLATES_DIR), filename)


def generated_docs_path(instance, filename):
    return os.path.join(str(settings.TEMPLATES_ADMIN_GENERATED_DOCS_DIR), filename)


class DatasourceRegistry(models.Model):
    name = models.CharField(max_length=255)
    api_endpoint = models.URLField()
    auth_token = models.CharField(max_length=512, blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class TemplateDocument(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    docx_file = models.FileField(upload_to=template_upload_path, blank=True, null=True)
    datasources = models.ManyToManyField('DatasourceRegistry', blank=True)

    def __str__(self):
        return self.name


class TemplateField(models.Model):
    FIELD_TYPES = [
        ('text', 'Texte'),
        ('number', 'Nombre'),
        ('date', 'Date'),
        ('choice', 'Choix'),
        ('table', 'Tableau'),
    ]
    document = models.ForeignKey(TemplateDocument, related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)               # identifiant du champ
    label = models.CharField(max_length=255, blank=True)  # affichage
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES)
    required = models.BooleanField(default=False)

    # datasource direct (simple)
    datasource = models.ForeignKey(DatasourceRegistry, null=True, blank=True, on_delete=models.SET_NULL)
    datasource_key = models.CharField(max_length=255, blank=True, null=True)  # jmespath expression

    # flag for tables and lists
    is_multiple = models.BooleanField(default=False)

    # options for choice fields or default table columns
    options = models.JSONField(blank=True, null=True)  # ex: ["a","b"] or [{"col1":...},...]
    order = models.PositiveIntegerField(default=0)

    # flag to know if the data is from a user input
    is_user_input = models.BooleanField(default=False)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.document.name}:{self.name}"


class FieldDatasourceMapping(models.Model):
    field = models.ForeignKey(TemplateField, related_name='mappings', on_delete=models.CASCADE)
    datasource = models.ForeignKey(DatasourceRegistry, on_delete=models.CASCADE)
    json_key = models.CharField(max_length=255)  # jmespath expression
    priority = models.IntegerField(default=0)

    class Meta:
        ordering = ['priority']

    def __str__(self):
        return f"{self.field} <= {self.datasource.name}:{self.json_key}"


class GeneratedDocument(models.Model):
    """
    Représente un document en cours de génération
    """
    template = models.ForeignKey("TemplateDocument", on_delete=models.CASCADE)
    context_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    output_file = models.FileField(upload_to=generated_docs_path, null=True, blank=True)

    def __str__(self):
        return f"Document #{self.id} ({self.template.name})"


class DocumentType(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    template = models.ForeignKey(
        TemplateDocument, on_delete=models.CASCADE,
        related_name="business_types"
    )
    # flag to determine if the document type is still available
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} -> {self.template.name}"
