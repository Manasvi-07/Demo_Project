from django.contrib import admin
from .models import Task

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


admin.site.register(Task, TaskAdmin)