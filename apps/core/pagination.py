from rest_framework.pagination import CursorPagination


# Курсорная пагинация: в запросе только закодированный курсор (?cursor=...),
# без номера страницы, смещения и общего количества записей
class DefaultCursorPagination(CursorPagination):
    page_size = 6
    # id — UUIDv7, он растёт со временем, поэтому '-id' = от новых к старым для любой модели
    ordering = '-id'
