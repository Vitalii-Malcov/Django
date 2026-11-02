from django.db import models
from django.utils import timezone

from apps.core.models.base import UUIDv7Model


# Менеджер по умолчанию: отдаёт только "неудалённые" категории
class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Category(UUIDv7Model):
    name = models.CharField(max_length=100, unique=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = CategoryManager()      # только неудалённые
    all_objects = models.Manager()   # все записи, включая "удалённые"

    class Meta:
        db_table = "task_manager_category"
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    # Мягкое удаление: запись остаётся в базе, но помечается как удалённая
    def delete(self, using=None, keep_parents=False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])
