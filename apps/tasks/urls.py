from django.urls import path
from rest_framework.routers import DefaultRouter

from apps.tasks.views.tasks_views import (
    get_task_by_project_name,
    TaskListCreateAPIView,
    TaskDetailAPIView,
    TaskStatsAPIView,
)
from apps.tasks.views.tag_views import TagListAPIView, TagDetailAPIView
from apps.tasks.views.subtask_views import SubTaskListCreateView, SubTaskDetailUpdateDeleteView
from apps.tasks.views.category_views import CategoryViewSet

app_name = 'tasks'

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task-list-create'),
    # stats и <uuid:pk> должны стоять ВЫШЕ <str:name>, иначе он их перехватит
    path('tasks/stats/', TaskStatsAPIView.as_view(), name='task-stats'),
    path('tasks/<uuid:pk>/', TaskDetailAPIView.as_view(), name='task-detail'),
    path('tasks/<str:name>/', get_task_by_project_name, name='get_task_by_project_name'),
    path('tags/', TagListAPIView.as_view(), name='tag-list'),
    path('tags/<uuid:pk>/', TagDetailAPIView.as_view(), name='tag-detail'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<uuid:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail'),
]

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
urlpatterns += router.urls
