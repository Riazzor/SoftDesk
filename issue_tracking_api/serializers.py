from rest_framework.serializers import ModelSerializer

from . import models


class ProjectSerializer(ModelSerializer):
    class Meta:
        model = models.Project
        fields = ["project_id", "title", "description", "type", "created_time", "updated_time"]
        read_only_fields = ["created_time", "updated_time"]


class IssueSerializer(ModelSerializer):
    project = ProjectSerializer

    class Meta:
        model = models.Issue
        fields = ["issue_id", "title", "description", "tag", "priority", "project", "status", "author_user", "assignee"]
        read_only_fields = ["created_time", "updated_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # we want a post with only the project id but the detail in list and detail.
        data["project"] = ProjectSerializer(instance.project).data
        return data

    def update(self, instance, validated_data):
        validated_data.pop("project", None)  # once created, can't change the project
        return super().update(instance, validated_data)


class CommentSerializer(ModelSerializer):
    issue = IssueSerializer

    class Meta:
        model = models.Comment
        fields = ["comment_id", "description", "author_user", "issue", "created_time", "updated_time"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # we want a post with only the issue id but the detail in list and detail.
        data["issue"] = IssueSerializer(instance.issue).data
        return data

    def update(self, instance, validated_data):
        validated_data.pop("issue", None)  # once created, can't change the issue
        return super().update(instance, validated_data)
