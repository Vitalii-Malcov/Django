from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import SubTask
from apps.tasks.serializers import SubTaskCreateSerializer


# Задание 5: создание и получение списка подзадач
class SubTaskListCreateView(APIView):
    def get_objects(self):
        return SubTask.objects.all()

    def get(self, request: Request) -> Response:
        subtasks = self.get_objects()
        serializer = SubTaskCreateSerializer(subtasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
