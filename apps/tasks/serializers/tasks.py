from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.tasks.models import Task
from apps.tasks.serializers.subtask_serializers import SubTaskSerializer


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        # due_date — это и есть "deadline" из задания; project обязателен в модели
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_at']


# Задание 3: задача со всеми связанными подзадачами
class TaskDetailSerializer(ModelSerializer):
    # related_name="subtasks" в модели SubTask
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'due_date',
                  'created_at', 'subtasks']


# Задание 4: дедлайн не может быть в прошлом
class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'due_date']
        read_only_fields = ['id']

    # В модели поле называется due_date, поэтому метод — validate_due_date
    def validate_due_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError('Дедлайн не может быть в прошлом.')
        return value
