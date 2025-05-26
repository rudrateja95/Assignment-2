from django.urls import path
from . import views

app_name = "tasks"

urlpatterns = [
    # API endpoints
    path("api/submit-task/", views.submit_task, name="submit_task"),
    path("api/task/<str:task_id>/", views.get_task_status, name="get_task_status"),
    path("api/tasks/", views.list_tasks, name="list_tasks"),
    path("api/retry-task/<str:task_id>/", views.retry_task, name="retry_task"),
    # Template views
    path("", views.dashboard, name="dashboard"),
    path("tasks-json/", views.get_tasks_json, name="get_tasks_json"),
]
