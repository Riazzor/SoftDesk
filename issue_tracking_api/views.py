from rest_framework import viewsets

from . import models, serializers

# Create your views here.


class ProjectAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class IssueAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.IssueSerializer

    def get_queryset(self):
        return models.Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentAPIViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(
            issue__project=self.kwargs['project_pk'],
            issue=self.kwargs['issue_pk'],
        )
