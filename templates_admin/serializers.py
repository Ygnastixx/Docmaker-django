from rest_framework import serializers
from .models import TemplateField, TemplateDocument


class FieldValueSerializer(serializers.Serializer):
    name = serializers.CharField()
    label = serializers.CharField()
    field_type = serializers.CharField()
    value = serializers.JSONField(allow_null=True)
    is_user_input = serializers.BooleanField(default=False)


class DocumentPrefillSerializer(serializers.Serializer):
    template = serializers.CharField()
    fields = FieldValueSerializer(many=True)


class TemplateFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemplateField
        fields = "__all__"


class DocumentTemplateSerializer(serializers.ModelSerializer):
    fields = TemplateFieldSerializer(many=True)

    class Meta:
        model = TemplateDocument
        fields = ["id", "name", "description", "docx_file", "fields"]