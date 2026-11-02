
"""Задание 10
1. Установите модуль djangorestframework.
2. Добавить этот модуль в файл requirements.txt.
3. Добавить этот модуль в список установленных приложений в файле settings.py.
4. Создать новый пакет serializers, в котором создать первый файл - projects
5. Импортируйте класс ModelSerializer.
6. Напишите первый сериализатор, который будет обрабатывать поля id и name для проекта,
выдавая общую базу для вывода всех проектов.
"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.projects.models import Project


class AllProjectsSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'created_at')


class CreateProjectSerializer(ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ('title', 'description', 'created_at')

    def validate_description(self, value: str) -> str:
        if len(value) < 30:
            raise serializers.ValidationError("Description must be at least 30 characters long")
        return value


class ProjectDetailSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'created_at', 'file_count')
