from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import Task
from apps.tasks.serializers import TaskSerializer


@api_view(['GET'])
def get_task_by_project_name(request: Request, name: str):
    try:
        task = Task.objects.filter(project__title=name)
        serializer = TaskSerializer(task, many=True)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    except Task.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)


# Задание 1 и 2: создание задачи (POST) и список задач (GET)
class TaskListCreateAPIView(APIView):
    def get_objects(self):
        return Task.objects.all()

    def get(self, request: Request) -> Response:
        tasks = self.get_objects()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Задание 2: получение конкретной задачи по её ID (UUID)
class TaskDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Task, pk=pk)

    def get(self, request: Request, pk) -> Response:
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Задание 3: статистика задач
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
