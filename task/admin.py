from django.contrib import admin
from .models import Task, TaskAttachment

class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'assigned',
        'created',
        'priority',
        'status',
        'due_date',
        'completed',
    )
    list_filter = ('priority', 'status', 'completed')
    search_fields = ('title', 'assigned__email', 'created__email')
    ordering = ('-due_date',)

class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('task', 'uploaded_at', 'file','image')

admin.site.register(Task, TaskAdmin)
admin.site.register(TaskAttachment, TaskAttachmentAdmin)