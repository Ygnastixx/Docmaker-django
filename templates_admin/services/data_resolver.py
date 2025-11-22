from .datasource_engine import DatasourceEngine


class DataResolver:
    def resolve(self, template, params=None) -> dict:
        context = {}
        for field in template.fields.all():
            if field.is_user_input:
                continue
            if field.datasource:
                engine = DatasourceEngine(field.datasource)
                data = engine.fetch(params=params)
                value = engine.extract_value(data, field.datasource_key)
                if field.is_multiple:
                    value = value or []
                else:
                    value = value or ""
                context[field.name] = value
        return context
