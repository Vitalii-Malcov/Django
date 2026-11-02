from datetime import datetime, timedelta

from django.utils import timezone
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.projects.models import Project
from apps.projects.serializers import (
    AllProjectsSerializer,
    CreateProjectSerializer,
    ProjectDetailSerializer,
)


class ProjectsListAPIView(APIView):

    def get_objects(self, date_from=None, date_to=None):
        projects = Project.objects.all()
        if date_from:
            start = timezone.make_aware(datetime.strptime(date_from, '%Y-%m-%d'))
            projects = projects.filter(created_at__gte=start)
        if date_to:
            end = timezone.make_aware(datetime.strptime(date_to, '%Y-%m-%d')) + timedelta(days=1)
            projects = projects.filter(created_at__lt=end)
        return projects

    def get(self, request: Request) -> Response:
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        try:
            projects = self.get_objects(date_from, date_to)
        except ValueError:
            return Response({"error": "Dates must be in format YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = AllProjectsSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = CreateProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Project, pk=pk)

    def get(self, request: Request, pk) -> Response:
        project = self.get_object(pk)
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        project = self.get_object(pk)
        serializer = CreateProjectSerializer(instance=project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        project = self.get_object(pk)
        project.delete()
        return Response({"message": "Project was deleted successfully"}, status=status.HTTP_200_OK)
