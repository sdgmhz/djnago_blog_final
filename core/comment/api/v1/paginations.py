from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """ a custom pagination for comments """
    page_size = 4
