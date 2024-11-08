from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'due_date', 'status', 'created_at', 'updated_at', 'user']

    def validate_status(self, value):
        if value not in ['TODO', 'IN_PROGRESS', 'DONE']:
            raise serializers.ValidationError("Invalid status")
        return value

class TaskListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'due_date', 'user']
