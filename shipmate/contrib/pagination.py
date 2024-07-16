from rest_framework.pagination import LimitOffsetPagination


class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 1000

    def get_offset(self, request):
        offset = super().get_offset(request)
        return max(0, offset - 1)
