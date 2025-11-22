from .data_resolver import DataResolver


class TemplatePrefillEngine:
    def __init__(self, template):
        self.template = template
        self.resolver = DataResolver()

    def prefill(self, params=None) -> dict:
        context = self.resolver.resolve(self.template, params=params)
        fields = []
        for field in self.template.fields.all():
            value = context.get(field.name)
            if field.is_user_input:
                value = None
            # fallback to options for choice fields
            elif field.field_type == 'choice' and field.options:
                if value not in field.options:
                    value = field.options

            fields.append({
                'name': field.name,
                'label': field.label or field.name,
                'field_type': field.field_type,
                'value': value,
                'is_user_input': field.is_user_input
            })
        return {"template": self.template.slug, "fields": fields}

