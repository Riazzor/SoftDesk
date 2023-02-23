from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import exceptions

from . import mixins, models, permissions, serializers


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
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def perform_create(self, serializer):
        serializer.save(author_user=self.request.user)


class ContributorAPIViewSet(mixins.IsContributorMixin, viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
    ]
    serializer_class = serializers.ContributorSerializer
    allowed_methods = ['GET', 'POST', 'DELETE']

    def get_queryset(self):
        project = models.Project.objects.get(project_id=self.kwargs['project_pk'])
        if not self.is_owner_or_contributor(project):
            raise exceptions.PermissionDenied(detail='Only available to contributors.')
        return models.Contributor.objects.filter(project=project)

    def retrieve(self, request, *args, **kwargs):
        # GET method is only for list. We don't want the detail.
        return self.http_method_not_allowed(request)

    def perform_create(self, serializer):
        serializer.save(
            project_id=self.kwargs["project_pk"],
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "project_pk": self.kwargs["project_pk"],
            }
        )
        print(context)
        return context


class IssueAPIViewSet(mixins.IsContributorMixin, viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly,
    ]
    serializer_class = serializers.IssueSerializer
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get_queryset(self):
        """
        Handling permission from here : current user needs to be in project contributors.
        Project needs to be fetched to compare contributors AND to check if issues are from
        the project so permission are handled here to fetch project only once.
        """
        project = models.Project.objects.get(project_id=self.kwargs['project_pk'])
        if not self.is_owner_or_contributor(project):
            raise exceptions.PermissionDenied(detail='Only available to contributors.')
        return project.issues.all()

    def perform_create(self, serializer):
        serializer.save(
            author_user=self.request.user,
            project_id=self.kwargs['project_pk'],
        )


class CommentAPIViewSet(mixins.IsContributorMixin, viewsets.ModelViewSet):
    permission_classes = [
        IsAuthenticated,
        permissions.IsOwnerOrReadOnly,
    ]
    serializer_class = serializers.CommentSerializer
    allowed_methods = ['GET', 'POST', 'PUT', 'DELETE']

    def get_queryset(self):
        project = models.Project.objects.get(project_id=self.kwargs['project_pk'])
        if not self.is_owner_or_contributor(project):
            raise exceptions.PermissionDenied(detail='Only available to contributors.')
        return models.Comment.objects.filter(
            issue__project=project,
            issue=self.kwargs['issue_pk'],
        )

    def perform_create(self, serializer):
        serializer.save(
            author_user=self.request.user,
            issue_id=self.kwargs['issue_pk'],
        )
