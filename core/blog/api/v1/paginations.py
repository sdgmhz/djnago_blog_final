from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """ a custom pagination for post and category"""
    page_size = 4
