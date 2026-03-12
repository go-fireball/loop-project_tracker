from django.urls import path

from .views import (
    dashboard,
    project_create,
    project_delete,
    project_detail,
    project_list,
    project_update,
    tag_create,
    tag_detail,
    tag_delete,
    tag_list,
    tag_update,
    task_create,
    task_delete,
    task_update,
)

app_name = "tracker"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("projects/", project_list, name="project_list"),
    path("projects/create/", project_create, name="project_create"),
    path("projects/<int:project_id>/", project_detail, name="project_detail"),
    path("projects/<int:project_id>/edit/", project_update, name="project_update"),
    path("projects/<int:project_id>/delete/", project_delete, name="project_delete"),
    path("projects/<int:project_id>/tasks/create/", task_create, name="task_create"),
    path("projects/<int:project_id>/tasks/<int:task_id>/edit/", task_update, name="task_update"),
    path("projects/<int:project_id>/tasks/<int:task_id>/delete/", task_delete, name="task_delete"),
    path("tags/", tag_list, name="tag_list"),
    path("tags/create/", tag_create, name="tag_create"),
    path("tags/<int:tag_id>/", tag_detail, name="tag_detail"),
    path("tags/<int:tag_id>/edit/", tag_update, name="tag_update"),
    path("tags/<int:tag_id>/delete/", tag_delete, name="tag_delete"),
]
