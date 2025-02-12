from rest_framework.pagination import PageNumberPagination
from django.conf import settings
from rest_framework.response import Response
from collections import OrderedDict


class CustomPageNumberPagination(PageNumberPagination):
    default_page_size = settings.REST_FRAMEWORK['PAGE_SIZE']
    
    def paginate_queryset(self, queryset, request, view=None):
        page_size = request.query_params.get("page_size", self.default_page_size)
        
        if page_size == "all":
            self.page_size = len(queryset)
        else:
            try:
                self.page_size = int(page_size)
            except ValueError:
                self.page_size = self.default_page_size
        
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        
        previous_page_number = self.page.previous_page_number() if self.page.has_previous() else None
        next_page_number = self.page.next_page_number() if self.page.has_next() else None
        
        return Response(
            OrderedDict(
                [
                    ("data", data),
                    ("page_size", len(data)), # 페이지 사이즈
                    ("total_count", self.page.paginator.count), # 데이터 총 수
                    ("total_page", self.page.paginator.num_pages), # 총 페이지 수
                    ("current_page", self.page.number), # 현재 페이지
                    ("next", self.get_next_link()),
                    ("next_page_number", next_page_number),
                    ("previous", self.get_previous_link()),
                    ("previous_page_number", previous_page_number),
                ]
            )
        )