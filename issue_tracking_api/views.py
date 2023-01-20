from rest_framework import viewsets

from . import models, serializers

# Create your views here.


class ProjectAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer


class IssueAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Issue.objects.all()
    serializer_class = serializers.IssueSerializer

    def get_queryset(self):
        return models.Issue.objects.filter(project=self.kwargs['project_pk'])
