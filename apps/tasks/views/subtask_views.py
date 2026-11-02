from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from apps.tasks.models import SubTask
from apps.tasks.serializers import SubTaskCreateSerializer


# Пагинация подзадач: не более 5 объектов на странице
class SubTaskPagination(PageNumberPagination):
    page_size = 5


# Задание 2: создание и список подзадач (Generic View)
class SubTaskListCreateView(ListCreateAPIView):
    serializer_class = SubTaskCreateSerializer
    pagination_class = SubTaskPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Фильтрация: ?status=new, ?due_date__gte=2026-11-01, ?due_date__lte=2026-11-30
    filterset_fields = {
        'status': ['exact'],
        'due_date': ['exact', 'gte', 'lte'],
    }
    # Поиск: ?search=продаж
    search_fields = ['title', 'description']
    # Сортировка: ?ordering=created_at; по умолчанию — от новых к старым
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = SubTask.objects.select_related('task').order_by('-created_at')

        # Из прошлой домашки: ?task_title=... — подзадачи главной задачи с таким названием
        task_title = self.request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title=task_title)

        return queryset


# Задание 2: получение, обновление и удаление подзадачи (Generic View)
class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
