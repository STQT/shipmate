from rest_framework.filters import OrderingFilter


def camelcase_to_snakecase(camelcase):
    snakecase = ''
    for char in camelcase:
        if char.isupper():
            snakecase += '_' + char.lower()
        else:
            snakecase += char
    return snakecase.lstrip('_')


class CamelCaseOrderingFilter(OrderingFilter):
    def get_ordering(self, request, queryset, view):
        # Get ordering fields from the request query parameters
        params = request.query_params.get(self.ordering_param)
        if params:
            fields = [param.strip() for param in params.split(",")]
            snakecase_fields = [camelcase_to_snakecase(field) for field in fields]
            return snakecase_fields
        return super().get_ordering(request, queryset, view)
