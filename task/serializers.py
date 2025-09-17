from rest_framework import serializers
from .models import Project, Task, TaskAttachment
from account.models import CustomUser
from account.enums import RoleChoices

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.id")

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'deadline', 'owner', 'created_at', 'updated_at']


class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'image','uploaded_at']
        read_only_fields = ['id','uploaded_at', 'task']

class TaskSerializer(serializers.ModelSerializer):
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    created = serializers.ReadOnlyField(source="created.id")

    class Meta:
        model = Task
        fields = ['id', 'project','title', 'description', 'status', 'priority', 'assigned', 'created','due_date', 'created_at', 'updated_at', 'attachments']

    def validate_assigned(self, value):
        if value is None:
            return value
        request = self.context['request']
        user = request.user

        if value.role == RoleChoices.ADMIN:
            raise serializers.ValidationError("Tasks cannot assigned to admin user")

        if user.role == RoleChoices.MANAGER:
            if value == user:
                raise serializers.ValidationError("Tasks cannot be assigned to manager users.")
            if value.role != RoleChoices.DEVELOPER:
                raise serializers.ValidationError("Managers can only assign tasks to developer.")
            
        if user.role == RoleChoices.DEVELOPER:
            raise serializers.ValidationError("developer are not allowed to assign tasks.")
        return value

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'image','uploaded_at']
        read_only_fields = ['id','uploaded_at', 'task']