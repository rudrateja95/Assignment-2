from rest_framework import serializers


class TaskSubmissionSerializer(serializers.Serializer):
    task_type = serializers.ChoiceField(
        choices=[
            ("word_count", "Word Count"),
            ("sentiment_analysis", "Sentiment Analysis"),
            ("character_count", "Character Count"),
            ("reverse_text", "Reverse Text"),
        ]
    )
    input_text = serializers.CharField(max_length=5000)


class TaskSerializer(serializers.Serializer):
    task_id = serializers.CharField()
    task_type = serializers.CharField()
    input_text = serializers.CharField()
    status = serializers.CharField()
    result = serializers.CharField(allow_null=True)
    submitted_at = serializers.DateTimeField()
    completed_at = serializers.DateTimeField(allow_null=True)
