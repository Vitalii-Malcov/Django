from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.tasks.models import Tag
from apps.tasks.serializers import TagSerializer


class TagListAPIView(APIView):
    def get_objects(self):
        return Tag.objects.all()

    def get(self, request: Request) -> Response:
        tags = self.get_objects()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = TagSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TagDetailAPIView(APIView):

    def get_object(self, pk):
        return get_object_or_404(Tag, pk=pk)

    def get(self, request: Request, pk) -> Response:
        tag = self.get_object(pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, pk) -> Response:
        tag = self.get_object(pk)
        serializer = TagSerializer(tag, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, pk) -> Response:
        tag = self.get_object(pk)
        tag.delete()
        return Response({"message": "Tag was deleted successfully"}, status=status.HTTP_200_OK)
