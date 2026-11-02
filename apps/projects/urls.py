from django.urls import path

from apps.projects.views.project_views import ProjectsListAPIView, ProjectDetailAPIView
from apps.projects.views.project_file_views import ProjectFileListAPIView

app_name = 'projects'

# urlpatterns = [
#     path('<str:name>/', hello, name='hello'),
# ]

"""Задание 11
1. Импортируйте ранее написанный сериализатор в файл, где будет реализовываться первое
представление.
2. Импортируйте дополнительные методы и классы:
○ Request из rest_framework (для типизации объекта запроса)
○ JsonResponse из django (для возврата и типизации ответов)
○ Status из rest_framework (для указания статусов ответов)
○ Api_view из rest_framework.decorators (для конкретики обрабатываемых методов)
○ Модель Project (для запросов к таблице проектов в базе данных)
3. Напишите функцию, которая будет обрабатывать GET запросы для получения списка всех проектов
из Базы данных.
4. Зарегистрировать эту функцию в списке эндпоинтов в файле urls.py
5. Проверьте работу готового эндпоинта."""


urlpatterns = [
    path('', ProjectsListAPIView.as_view(), name='project-list'),
    path('files/', ProjectFileListAPIView.as_view(), name='project-file-list'),
    path('<uuid:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),

]
