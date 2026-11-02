from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer, TaskDetailSerializer


@api_view(['GET'])
def get_task_by_project_name(request: Request, name: str):
    try:
        task = Task.objects.filter(project__title=name)
        serializer = TaskSerializer(task, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


# Номера дней недели для лукапа __week_day в Django: 1 = воскресенье ... 7 = суббота
WEEKDAYS = {
    'воскресенье': 1, 'sunday': 1,
    'понедельник': 2, 'monday': 2,
    'вторник': 3, 'tuesday': 3,
    'среда': 4, 'wednesday': 4,
    'четверг': 5, 'thursday': 5,
    'пятница': 6, 'friday': 6,
    'суббота': 7, 'saturday': 7,
}


# Задание 1: создание и список задач (Generic View)
class TaskListCreateAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Фильтрация: ?status=new, ?due_date__gte=2026-11-01, ?due_date__lte=2026-11-30
    # (due_date — это "deadline" из задания)
    filterset_fields = {
        'status': ['exact'],
        'due_date': ['exact', 'gte', 'lte'],
    }
    # Поиск: ?search=отчёт
    search_fields = ['title', 'description']
    # Сортировка: ?ordering=created_at или ?ordering=-created_at
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = Task.objects.all()

        # Из прошлой домашки: ?day=вторник — задачи со сроком в этот день недели
        day = self.request.query_params.get('day')
        if day:
            week_day = WEEKDAYS.get(day.strip().lower())
            if week_day is None:
                raise ValidationError({'day': f'Неизвестный день недели: {day}'})
            queryset = queryset.filter(due_date__week_day=week_day)

        return queryset


# Задание 1: получение, обновление и удаление задачи (Generic View)
class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer


# Статистика задач — оставлена как есть
class TaskStatsAPIView(APIView):
    def get(self, request: Request) -> Response:
        # Общее количество задач
        total_tasks = Task.objects.count()

        # Количество задач по каждому статусу: {"new": 3, "done": 1, ...}
        tasks_by_status = {
            item['status']: item['count']
            for item in Task.objects.values('status').annotate(count=Count('id'))
        }

        # Просроченные: срок прошёл, а задача ещё не выполнена
        overdue_tasks = (
            Task.objects.filter(due_date__lt=timezone.now())
            .exclude(status=Task.Status.DONE)
            .count()
        )

        return Response({
            'total_tasks': total_tasks,
            'tasks_by_status': tasks_by_status,
            'overdue_tasks': overdue_tasks,
        }, status=status.HTTP_200_OK)
