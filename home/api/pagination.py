from rest_framework.pagination import CursorPagination


class PostCursorPagination(CursorPagination):
    ordering = '-when_posted'