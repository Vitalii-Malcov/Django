from rest_framework import serializers

from apps.tasks.models import SubTask


# Задание 1: created_at переопределено как поле только для чтения
class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'task', 'status', 'due_date', 'created_at']


# Задание 3: сериализатор подзадачи для вложения в TaskDetailSerializer
class SubTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_at']
