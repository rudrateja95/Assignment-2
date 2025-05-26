import pymongo
from django.conf import settings
from datetime import datetime
import uuid


def get_mongodb_connection():
    """Get MongoDB connection"""
    client = pymongo.MongoClient(
        host=settings.MONGODB_SETTINGS["host"], port=settings.MONGODB_SETTINGS["port"]
    )
    db = client[settings.MONGODB_SETTINGS["db"]]
    return db


def create_task(task_type, input_text):
    """Create a new task in MongoDB"""
    db = get_mongodb_connection()
    tasks_collection = db.tasks

    task_data = {
        "task_id": str(uuid.uuid4()),
        "task_type": task_type,
        "input_text": input_text,
        "status": "PENDING",
        "result": None,
        "submitted_at": datetime.utcnow(),
        "completed_at": None,
    }

    result = tasks_collection.insert_one(task_data)
    task_data["_id"] = str(result.inserted_id)
    return task_data


def get_task_by_id(task_id):
    """Get task by task_id from MongoDB"""
    db = get_mongodb_connection()
    tasks_collection = db.tasks

    task = tasks_collection.find_one({"task_id": task_id})
    if task:
        task["_id"] = str(task["_id"])
    return task


def update_task_status(task_id, status, result=None, completed_at=None):
    """Update task status in MongoDB"""
    db = get_mongodb_connection()
    tasks_collection = db.tasks

    update_data = {"status": status}
    if result is not None:
        update_data["result"] = result
    if completed_at is not None:
        update_data["completed_at"] = completed_at

    result = tasks_collection.update_one({"task_id": task_id}, {"$set": update_data})
    return result.modified_count > 0


def get_all_tasks():
    """Get all tasks from MongoDB"""
    db = get_mongodb_connection()
    tasks_collection = db.tasks

    tasks = list(tasks_collection.find().sort("submitted_at", -1))
    for task in tasks:
        task["_id"] = str(task["_id"])
    return tasks
