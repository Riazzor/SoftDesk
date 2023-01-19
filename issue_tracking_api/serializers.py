from rest_framework.serializers import ModelSerializer

from .models import Project


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = Project
        fields = ["title", "description", "type", "created_time", "updated_time"]
        read_only_fields = ["created_time", "updated_time"]
