from django.db import models
from account.models import CustomUser
from task.enums import StatusChoice, PriorityChoice

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Project(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    deadline = models.DateTimeField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="project_owned")

    def __str__(self):
        return self.title

class Task(BaseModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=50, choices=StatusChoice, default=StatusChoice.TODO)
    priority = models.CharField(max_length=50, choices=PriorityChoice, default=PriorityChoice.MEDIUM)
    assigned = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='assigned_tasks')
    created = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    due_date = models.DateTimeField()

    def __str__(self):
        return f"{self.title}({self.project.title})"