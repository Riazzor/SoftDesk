from django.urls import include, path

from rest_framework_nested import routers

from . import views


router = routers.SimpleRouter()
router.register("projects", views.ProjectAPIViewSet, basename="projects")

project_router = routers.NestedSimpleRouter(router, "projects", lookup="project")
project_router.register("issues", views.IssueAPIViewSet, basename="issues")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/", include(project_router.urls)),
]
