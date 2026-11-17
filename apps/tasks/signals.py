from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from apps.tasks.models import Task


@receiver(pre_save, sender=Task)
def remember_old_status(sender, instance, **kwargs):
    # id (UUIDv7) задаётся до сохранения, поэтому смотрим, есть ли задача в базе
    instance._old_status = Task.objects.filter(pk=instance.pk).values_list('status', flat=True).first()


@receiver(post_save, sender=Task)
def send_status_changed_email(sender, instance, created, **kwargs):
    # Новая задача — это не смена статуса
    if created:
        return
    # Статус не изменился — письмо не нужно
    if instance._old_status == instance.status:
        return
    # Некому отправлять
    if instance.owner is None or not instance.owner.email:
        return

    is_done = instance.status == Task.Status.DONE
    if is_done:
        subject = f'Задача закрыта: {instance.title}'
    else:
        subject = f'Статус задачи изменён: {instance.title}'

    message = render_to_string('tasks/emails/task_status_changed.txt', {
        'task': instance,
        'old_status': dict(Task.Status.choices).get(instance._old_status),
        'is_done': is_done,
    })
    send_mail(
        subject,
        message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[instance.owner.email],
    )
