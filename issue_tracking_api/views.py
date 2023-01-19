from rest_framework import viewsets

from . import models, serializers

# Create your views here.


class ProjectAPIViewSet(viewsets.ModelViewSet):
    queryset = models.Project.objects.all()
    serializer_class = serializers.ProjectSerializer
