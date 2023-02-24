from django.urls import include, path

from rest_framework_nested import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views


router = routers.SimpleRouter()
router.register("projects", views.ProjectAPIViewSet, basename="projects")

project_router = routers.NestedSimpleRouter(router, "projects", lookup="project")
project_router.register("issues", views.IssueAPIViewSet, basename="issues")
project_router.register("contributors", views.ContributorAPIViewSet, basename="contributor")

issue_router = routers.NestedSimpleRouter(project_router, "issues", lookup="issue")
issue_router.register("comments", views.CommentAPIViewSet, basename="comments")

urlpatterns = [
    path("signup/", views.RegisterView.as_view(), name="signup"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token_refresh"),

    path("", include(router.urls)),
    path("", include(project_router.urls)),
    path("", include(issue_router.urls)),
    path("projects/<int:project_pk>/contributors/", views.ContributorAPIViewSet.as_view({'get': 'list'}), name="contributors"),
]
