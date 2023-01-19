from django.urls import include, path

from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register("projects", views.ProjectAPIViewSet, basename="projects")

urlpatterns = [
    path("api/", include(router.urls)),
]
