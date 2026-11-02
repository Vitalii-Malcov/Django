from django.db.models import Count
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tasks.models import Category
from apps.tasks.serializers import CategoryCreateSerializer


# Задание 1: полный CRUD для категорий
class CategoryViewSet(ModelViewSet):
    # Category.objects — менеджер без "удалённых" категорий
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    # GET .../categories/count_tasks/ — количество задач в каждой категории
    @action(detail=False, methods=['get'])
    def count_tasks(self, request: Request) -> Response:
        # Task.categories — ManyToMany без related_name, обратное имя для запросов — "task"
        categories = self.get_queryset().annotate(tasks_count=Count('task'))
        data = [
            {'id': category.id, 'name': category.name, 'tasks_count': category.tasks_count}
            for category in categories
        ]
        return Response(data)
