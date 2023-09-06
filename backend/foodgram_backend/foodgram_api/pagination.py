from rest_framework.pagination import PageNumberPagination


class PaginatorUser(PageNumberPagination):
    page_size_query_param = 'limit'
