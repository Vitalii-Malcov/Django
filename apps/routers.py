from django.urls import include, path

urlpatterns = [
    path('tasks/', include('apps.tasks.urls')),
    path('auth/', include('apps.users.urls')),
    path('projects/', include('apps.projects.urls')),
]
