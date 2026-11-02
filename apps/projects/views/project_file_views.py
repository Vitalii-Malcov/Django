from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.projects.models import Project, ProjectFile
from apps.projects.serializers import AllProjectFilesSerializer, CreateProjectFileSerializer


class ProjectFileListAPIView(APIView):
    def get_objects(self, project_name=None):
        if project_name:
            return ProjectFile.objects.filter(projects__title=project_name)
        return ProjectFile.objects.all()

    def get(self, request: Request) -> Response:
        project_name = request.query_params.get('project')
        files = self.get_objects(project_name)
        serializer = AllProjectFilesSerializer(files, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        file = request.FILES.get('file')
        project_id = request.data.get('project_id')
        if not file or not project_id:
            return Response({"error": "Fields 'file' and 'project_id' are required."}, status=status.HTTP_400_BAD_REQUEST)
        project = get_object_or_404(Project, pk=project_id)
        serializer = CreateProjectFileSerializer(data=request.data, context={"raw_file": file})
        serializer.is_valid(raise_exception=True)
        project_file = serializer.save()
        project_file.projects.set([project])
        return Response({"message": "File upload successfully"}, status=status.HTTP_201_CREATED)
