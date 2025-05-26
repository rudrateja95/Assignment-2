from django.db import models
from datetime import datetime
import uuid


# Django model for reference (not used directly)
class TaskModel(models.Model):
    task_id = models.CharField(max_length=100, unique=True)
    task_type = models.CharField(max_length=50)
    input_text = models.TextField()
    status = models.CharField(max_length=20, default="PENDING")
    result = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tasks_reference"
