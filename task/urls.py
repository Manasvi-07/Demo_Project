from django.urls import path
from .views import ProjectView, ProjectDetailsView, TaskView, TaskDetailsView

urlpatterns = [
    path('projects/', ProjectView.as_view(), name="Project_create_list"),
    path('projects/<int:pk>/', ProjectDetailsView.as_view(), name="Project_details_update_delete"),
    path('tasks/', TaskView.as_view(), name="Task_list_create"),
    path('tasks/<int:pk>/', TaskDetailsView.as_view(), name="task_details_update_detelet"),
]