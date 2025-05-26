from celery import shared_task
from .utils import get_task_by_id, update_task_status
from datetime import datetime
import time
from textblob import TextBlob


@shared_task(bind=True)
def process_task(self, task_id):
    """Process a task based on its type"""
    try:
        # Get task from MongoDB
        task = get_task_by_id(task_id)
        if not task:
            return f"Task {task_id} not found"

        # Update status to IN_PROGRESS
        update_task_status(task_id, "IN_PROGRESS")

        # Process based on task type
        task_type = task["task_type"]
        input_text = task["input_text"]

        if task_type == "word_count":
            result = count_words(input_text)
        elif task_type == "sentiment_analysis":
            result = analyze_sentiment(input_text)
        elif task_type == "character_count":
            result = count_characters(input_text)
        elif task_type == "reverse_text":
            result = reverse_text(input_text)
        else:
            result = f"Unknown task type: {task_type}"

        # Simulate processing time
        time.sleep(2)

        # Update task with result
        update_task_status(
            task_id, "COMPLETED", result=str(result), completed_at=datetime.utcnow()
        )

        return f"Task {task_id} completed successfully"

    except Exception as e:
        # Update task status to FAILED
        update_task_status(
            task_id, "FAILED", result=f"Error: {str(e)}", completed_at=datetime.utcnow()
        )
        return f"Task {task_id} failed: {str(e)}"


def count_words(text):
    """Count words in text"""
    words = text.strip().split()
    return {"word_count": len(words), "original_text": text}


def analyze_sentiment(text):
    """Analyze sentiment using TextBlob"""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    if polarity > 0.1:
        sentiment = "Positive"
    elif polarity < -0.1:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "polarity": round(polarity, 3),
        "original_text": text,
    }


def count_characters(text):
    """Count characters in text"""
    return {
        "character_count": len(text),
        "character_count_no_spaces": len(text.replace(" ", "")),
        "original_text": text,
    }


def reverse_text(text):
    """Reverse the text"""
    return {"reversed_text": text[::-1], "original_text": text}
