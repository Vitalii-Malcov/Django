from rest_framework import serializers

from apps.tasks.models import Category


# Задание 2: проверка уникальности названия в create и update
class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        # Отключаем встроенную проверку unique, чтобы её делали наши create/update
        extra_kwargs = {'name': {'validators': []}}

    def create(self, validated_data):
        if Category.objects.filter(name=validated_data['name']).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().create(validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get('name', instance.name)
        # Исключаем саму обновляемую категорию из проверки
        if Category.objects.filter(name=name).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError({'name': 'Категория с таким названием уже существует.'})
        return super().update(instance, validated_data)
