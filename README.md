# 🧠 Task Manager Backend

A Django-based backend for managing tasks with support for asynchronous processing using Celery + Redis and MongoDB for document storage.

---


This is a backend system built with Django REST Framework to manage tasks, demonstrate async processing using Celery, and optionally integrate MongoDB for document storage (e.g. task attachments).

Key features:
- Django REST API
- Task handling via Celery workers
- Redis as a broker
- MongoDB integration
- Dockerized setup
- Modular and well-documented code

---



### Prerequisites

- Python 3.10+
- Redis server running (locally or via Docker)
- MongoDB
- `pip`, `virtualenv`

### 🔧 Local Installation

```bash
git clone <your-repo-url>
cd task_manager

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
cd backend
python manage.py migrate

# Run development server
python manage.py runserver
