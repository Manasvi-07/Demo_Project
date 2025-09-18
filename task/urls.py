from django.urls import path
from .views import ProjectView, ProjectDetailsView, TaskView, TaskDetailsView, TaskAttachmentUploadView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name="project_create_list"),
    path('projects/<int:pk>/', ProjectDetailsView.as_view(), name="project_details_update_delete"),
    path('tasks/', TaskView.as_view(), name="task_list_create"),
    path('tasks/<int:pk>/', TaskDetailsView.as_view(), name="task_details_update_detelet"),
    path('tasks/attachments/<int:task_id>/', TaskAttachmentUploadView.as_view(), name="task_file_attachments")
]