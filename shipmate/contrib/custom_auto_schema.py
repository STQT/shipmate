from drf_spectacular.openapi import AutoSchema
from rest_framework.parsers import MultiPartParser


class CustomAutoSchema(AutoSchema):
    def _get_pagination_parameters(self):
        paginator = getattr(self.view, 'pagination_class', None)
        if paginator and self._is_list_view(paginator):
            return {
                'name': paginator.page_query_param,
                'in': 'query',
                'required': False,
                'description': 'Page number',
                'schema': {
                    'type': 'integer',
                    'default': 1
                }
            }, {
                'name': paginator.page_size_query_param,
                'in': 'query',
                'required': False,
                'description': 'Number of items per page',
                'schema': {
                    'type': 'integer',
                    'default': paginator.page_size
                }
            }
        return super()._get_pagination_parameters()

    # def _get_examples(self, serializer, direction, media_type, status_code=None, extras=None):
    #     """Override this method to customize example generation."""
    #     # Your custom logic for example generation
    #     x = super()._get_examples(serializer, direction, media_type, status_code, extras)
    #     if self._is_list_view() and self.view.pagination_class:
    #         print(self.view.pagination_class)
    #         print(x)
    #     return x


from drf_spectacular.generators import SchemaGenerator


class CustomSchemaGenerator(SchemaGenerator):
    # Override the get_parser_classes method to include your custom parser
    def get_request_body_content(self, *args, **kwargs):
        print("EEEEEEE")
        content = super().get_request_body_content(*args, **kwargs)
        # Change the default content type to 'multipart/form-data'
        content['multipart/form-data'] = content.pop('application/json', None)
        return content


