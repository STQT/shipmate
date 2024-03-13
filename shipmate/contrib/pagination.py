from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 10  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Maximum number of items per page

    def get_paginated_response(self, data):
        return Response({
            'currentPage': self.page.number,
            'data': data,
            'totalPages': self.page.paginator.num_pages,
            'totalData': self.page.paginator.count
        })
