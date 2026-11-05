"""
Домашнее задание: Проект "Менеджер задач" — ORM запросы (CRUD для Task и SubTask).

Запуск (PowerShell):
    Get-Content orm_queries.py -Encoding UTF8 | python manage.py shell
"""
from datetime import timedelta

from django.utils import timezone

from tasks.models import Task, SubTask, Status

now = timezone.now()

# ---------- 1. Создание записей ----------
task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    status=Status.NEW,
    deadline=now + timedelta(days=3),
)

SubTask.objects.create(
    title="Gather information",
    description="Find necessary information for the presentation",
    status=Status.NEW,
    deadline=now + timedelta(days=2),
    task=task,
)

SubTask.objects.create(
    title="Create slides",
    description="Create presentation slides",
    status=Status.NEW,
    deadline=now + timedelta(days=1),
    task=task,
)

# ---------- 2. Чтение записей ----------
# Задачи со статусом "New"
print("Tasks New:", Task.objects.filter(status=Status.NEW))

# Подзадачи со статусом "Done", у которых срок выполнения истёк
print("SubTasks Done overdue:", SubTask.objects.filter(status=Status.DONE, deadline__lt=timezone.now()))

# ---------- 3. Изменение записей ----------
# Статус "Prepare presentation" -> "In progress"
print("Updated task status:",
      Task.objects.filter(title="Prepare presentation").update(status=Status.IN_PROGRESS))

# Срок "Gather information" -> два дня назад
print("Updated deadline:",
      SubTask.objects.filter(title="Gather information").update(deadline=timezone.now() - timedelta(days=2)))

# Новое описание для "Create slides"
print("Updated description:",
      SubTask.objects.filter(title="Create slides").update(description="Create and format presentation slides"))

# ---------- 4. Удаление записей ----------
# Удаляем задачу и все её подзадачи (on_delete=CASCADE)
print("Deleted:", Task.objects.filter(title="Prepare presentation").delete())
