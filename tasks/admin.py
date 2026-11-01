from django.contrib import admin, messages

from tasks.models import Category, SubTask, Task, Status


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name",)


class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title","status","deadline","description")



@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("short_title", "deadline", "status", "created_at")
    list_filter = ("status", "categories")
    search_fields = ("title",)
    inlines = [SubTaskInline,]

    @admin.display(description="Title", ordering="title")
    def short_title(self, obj):
        if len(obj.title) > 10:
            return f"{obj.title[:10]}"
        return obj.title


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "task", "status", "deadline", "created_at")
    list_filter = ("status",)
    actions = ["mark_as_done"]

    @admin.action(description="Перевести выбранные подзадачи в статус - Done")
    def mark_as_done(self, request, queryset):
        updated_count = queryset.update(status=Status.DONE)
        self.message_user(
            request,
            f"Переведено статус Done подзадач: {updated_count}.",
            messages.SUCCESS,
        )
