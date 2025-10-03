from celery import shared_task
from django.core.mail import send_mail
from task.models import Task
from django.conf import settings
from task.utils import notify_task_update

@shared_task
def send_mail_task_notification(task_id):
    try : 
        task = Task.objects.select_related('created', 'project').prefetch_related('assigned').get(id=task_id)

        for user in task.assigned.all():
            if user.email:
                subject = f"New Task Assigned: {task.title}"
                message = f"{task.description}\n\n Due: {task.due_date.strftime('%Y-%m-%d %H:%M')}"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [user.email]
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return f"Emails sent to {[u.email for u in task.assigned.all() if u.email]}"

    except Task.DoesNotExist:
        return "Task not found"

@shared_task 
def daily_task_reminder():
    task = Task.objects.filter(
        completed=False,
        assigned__isnull=False,
        assigned__email__isnull=False,
    ).select_related("created", "project").prefetch_related("assigned")

    count = 0
    for task in task:
        subject = f"New Task Assigned : {task.title}"
        message = f"{task.description}\n\n Due : {task.due_date.strftime('%Y-%m-%d %H:%M')}"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [task.assigned.email]
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        notify_task_update(task)
        count += 1

    print(f"Reminder task complete. Total reminders sent: {count}")
    return f"Reminders sent for {count} task(s)"