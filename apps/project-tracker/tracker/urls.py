from django.urls import path

from .views import (
    dashboard,
    project_create,
    project_delete,
    project_detail,
    project_list,
    project_update,
    tag_detail,
)

app_name = "tracker"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("projects/", project_list, name="project_list"),
    path("projects/create/", project_create, name="project_create"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("projects/<int:project_id>/edit/", project_update, name="project_update"),
    path("projects/<int:project_id>/delete/", project_delete, name="project_delete"),
    path("tags/<int:tag_id>/", tag_detail, name="tag_detail"),
]
