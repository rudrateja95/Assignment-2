from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from .serializers import TaskSubmissionSerializer, TaskSerializer
from .utils import create_task, get_task_by_id, get_all_tasks
from .tasks import process_task
import json


@api_view(["POST"])
def submit_task(request):
    """Submit a new task"""
    serializer = TaskSubmissionSerializer(data=request.data)

    if serializer.is_valid():
        task_type = serializer.validated_data["task_type"]
        input_text = serializer.validated_data["input_text"]

        # Create task in MongoDB
        task = create_task(task_type, input_text)

        # Queue the task with Celery
        process_task.delay(task["task_id"])

        return Response(
            {
                "message": "Task submitted successfully",
                "task_id": task["task_id"],
                "status": task["status"],
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_task_status(request, task_id):
    """Get task status and result"""
    task = get_task_by_id(task_id)

    if not task:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = TaskSerializer(task)
    return Response(serializer.data)


@api_view(["GET"])
def list_tasks(request):
    """List all tasks"""
    tasks = get_all_tasks()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def retry_task(request, task_id):
    """Retry a failed task"""
    task = get_task_by_id(task_id)

    if not task:
        return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    if task["status"] not in ["FAILED", "COMPLETED"]:
        return Response(
            {"error": "Can only retry failed or completed tasks"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Update status to PENDING and queue again
    from .utils import update_task_status

    update_task_status(task_id, "PENDING")

    # Queue the task with Celery
    process_task.delay(task_id)

    return Response({"message": "Task queued for retry", "task_id": task_id})


# Template views
def dashboard(request):
    """Dashboard view with Django templates"""
    return render(request, "tasks/dashboard.html")


def get_tasks_json(request):
    """Get tasks as JSON for AJAX calls"""
    tasks = get_all_tasks()

    # Convert datetime objects to strings for JSON serialization
    for task in tasks:
        if task.get("submitted_at"):
            task["submitted_at"] = task["submitted_at"].isoformat()
        if task.get("completed_at"):
            task["completed_at"] = task["completed_at"].isoformat()

    return JsonResponse({"tasks": tasks})
