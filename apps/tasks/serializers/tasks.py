from rest_framework.serializers import ModelSerializer
from apps.tasks.models import Task


class TaskSerializer(ModelSerializer):
    class Meta:
        model = Task
        # due_date — это и есть "deadline" из задания; project обязателен в модели
        fields = ['id', 'title', 'description', 'status', 'priority', 'project', 'due_date', 'created_at']
        read_only_fields = ['id', 'created_at']
