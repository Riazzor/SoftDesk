from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from . import models, permissions, serializers

# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterSerializer


class ProjectAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly,
    ]
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class IssueAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly,
    ]
    serializer_class = serializers.IssueSerializer

    def get_queryset(self):
        return models.Issue.objects.filter(project=self.kwargs['project_pk'])


class CommentAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly,
    ]
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(
            issue__project=self.kwargs['project_pk'],
            issue=self.kwargs['issue_pk'],
        )
