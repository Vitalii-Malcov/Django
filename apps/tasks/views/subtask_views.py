from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import SubTask
from apps.tasks.serializers import SubTaskCreateSerializer


# Пагинация подзадач: не более 5 объектов на странице
class SubTaskPagination(PageNumberPagination):
    page_size = 5


# Создание подзадачи (POST) и список подзадач (GET) с фильтрами и пагинацией
class SubTaskListCreateView(APIView):
    def get_objects(self, request: Request):
        # От самой последней добавленной подзадачи к самой первой
        queryset = SubTask.objects.select_related('task').order_by('-created_at')

        # ?task_title=... — подзадачи главной задачи с таким названием
        task_title = request.query_params.get('task_title')
        if task_title:
            queryset = queryset.filter(task__title=task_title)

        # ?status=... — подзадачи с этим статусом
        subtask_status = request.query_params.get('status')
        if subtask_status:
            queryset = queryset.filter(status=subtask_status)

        return queryset

    def get(self, request: Request) -> Response:
        queryset = self.get_objects(request)
        paginator = SubTaskPagination()
        page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = SubTaskCreateSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = SubTaskCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# Задание 5: получение, обновление и удаление подзадачи
class SubTaskDetailUpdateDeleteView(APIView):
    def get_object(self, pk):
        return get_object_or_404(SubTask, pk=pk)

    def get(self, request: Request, pk) -> Response:
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        subtask = self.get_object(pk)
        serializer = SubTaskCreateSerializer(subtask, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        subtask = self.get_object(pk)
        subtask.delete()
        return Response({'message': 'SubTask was deleted successfully'}, status=status.HTTP_200_OK)
