from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Project, Task, TaskAttachment
from task.serializers import ProjectSerializer, TaskSerializer, TaskAttachmentSerializer
from task.permissions import IsAdminOrManager, IsAdminManagerOrTaskOwner
from account.enums import RoleChoices
import logging
from task.tasks import send_mail_task_notification
from task.utils import notify_task_update
from drf_spectacular.utils import extend_schema
from . import serializers

logger = logging.getLogger("task")

class ProjectView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all().order_by('id')

    def get_queryset(self):
        user = self.request.user
        if user.role == RoleChoices.ADMIN:
            return Project.objects.all()
        return Project.objects.filter(owner=user)

    def perform_create(self, serializer):
        if self.request.user.role == RoleChoices.DEVELOPER:
            raise PermissionDenied("Developer can not create project")
        serializer.save(owner=self.request.user)

class ProjectDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Project.objects.all()

class TaskView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrManager]
    queryset = Project.objects.all().order_by('id')

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project", "due_date", "status", "priority"]
    ordering_fields = ["due_date", "priority", "created_at"]
    search_fields = ['title', "description", "assigned__email"]

    def perform_create(self, serializer):
        task = serializer.save(created=self.request.user)
        logger.info(
            f"Task created: {task.title} "
            f"(Project: {task.project.title if task.project else 'No Project'}, "
            f"Assigned: {task.assigned.email if task.assigned else 'Unassigned'}) "
            f"created {self.request.user.email}"
        )
        send_mail_task_notification.delay(task.id)
        notify_task_update(task)
        
    def get_queryset(self):
        user = self.request.user
        queryset = Task.objects.select_related("assigned","created", "project").order_by("-created_at")

        if user.role == RoleChoices.ADMIN:
            logger.info(f"Admin {user.email} view all task")
            return queryset
        elif user.role == RoleChoices.MANAGER:
            logger.info(f"Manager {user.email} show only owned task created")
            return queryset.filter(project__owner=user)
        logger.info(f"Developer {user.email} show only owned assigned task")
        return queryset.filter(assigned=user)           
    
class TaskDetailsView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated,IsAdminManagerOrTaskOwner]
    queryset = Task.objects.all()

class TaskAttachmentUploadView(generics.CreateAPIView):
    queryset = TaskAttachment.objects.all()
    serializer_class = TaskAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(request=serializers.TaskAttachmentSerializer, responses=TaskAttachmentSerializer)
    def perform_create(self, serializer):
        task_id = self.kwargs.get("task_id")
        task = Task.objects.get(id=task_id)
        serializer.save(task=task)