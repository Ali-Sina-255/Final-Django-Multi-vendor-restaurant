from rest_framework.pagination import PageNumberPagination


class DefaultPaginationClass(PageNumberPagination):
    page_size = 4


class CartItemPaginationClass(PageNumberPagination):
    page_size = 4
