from rest_framework import serializers

from apps.tasks.models import Category


# Проверка уникальности названия в create и update
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        # Отключаем встроенную проверку unique, чтобы её делали наши create/update
        extra_kwargs = {'name': {'validators': []}}

    # all_objects — с учётом "удалённых": имя у них в базе остаётся занятым (unique=True)
    def create(self, validated_data):
        if Category.all_objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        # Исключаем саму обновляемую категорию из проверки
        if Category.all_objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().update(instance, validated_data)
