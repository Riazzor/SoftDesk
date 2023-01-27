from django.urls import include, path

from rest_framework_nested import routers

from . import views


router = routers.SimpleRouter()
router.register("projects", views.ProjectAPIViewSet, basename="projects")

project_router = routers.NestedSimpleRouter(router, "projects", lookup="project")
project_router.register("issues", views.IssueAPIViewSet, basename="issues")

issue_router = routers.NestedSimpleRouter(project_router, "issues", lookup="issue")
issue_router.register("comments", views.CommentAPIViewSet, basename="comments")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(project_router.urls)),
    path("api/", include(issue_router.urls)),
]
