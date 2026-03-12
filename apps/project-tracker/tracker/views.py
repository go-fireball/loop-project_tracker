from django.db.models import Count, Prefetch, Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from .forms import ProjectForm
from .models import Project, Tag, Task


def _project_list_queryset():
    return (
        Project.objects.annotate(
            task_count=Count("tasks", distinct=True),
            open_task_count=Count(
                "tasks",
                filter=~Q(tasks__status=Task.STATUS_DONE),
                distinct=True,
            ),
        )
        .prefetch_related("tags")
        .order_by("name")
    )


def _recent_projects_queryset():
    return Project.objects.prefetch_related("tags").order_by("-created_date", "name")[:5]


def _project_detail_queryset():
    return Project.objects.prefetch_related(
        "tags",
        Prefetch("tasks", queryset=Task.objects.prefetch_related("tags").order_by("due_date", "title")),
    )


def _dashboard_context(form=None):
    task_counts = {
        row["status"]: row["count"]
        for row in Task.objects.values("status")
        .annotate(count=Count("id"))
        .order_by("status")
    }
    return {
        "page_title": "Project Tracker",
        "project_form": form or ProjectForm(),
        "project_create_url": reverse("tracker:project_create"),
        "total_projects": Project.objects.count(),
        "task_counts": [
            {
                "value": task_counts.get(status, 0),
                "label": label,
                "status": status,
            }
            for status, label in Task.STATUS_CHOICES
        ],
        "overdue_task_count": Task.objects.filter(
            due_date__lt=timezone.localdate()
        ).exclude(status=Task.STATUS_DONE).count(),
        "recent_projects": _recent_projects_queryset(),
    }


def _project_list_context(form=None):
    return {
        "page_title": "Projects",
        "project_form": form or ProjectForm(),
        "project_create_url": reverse("tracker:project_create"),
        "projects": _project_list_queryset(),
    }


def _render_mutation_response(request, replacements, status=200):
    rendered_replacements = [
        {
            "selector": selector,
            "html": render_to_string(template_name, context, request=request),
        }
        for selector, template_name, context in replacements
    ]
    return render(
        request,
        "tracker/partials/project_mutation_response.html",
        {"replacements": rendered_replacements},
        status=status,
    )


def _project_form_context(form, source_page, action, heading, submit_label):
    return {
        "form": form,
        "source_page": source_page,
        "form_action": action,
        "form_heading": heading,
        "form_submit_label": submit_label,
    }


def dashboard(request):
    return render(request, "tracker/dashboard.html", _dashboard_context())


def project_list(request):
    return render(request, "tracker/project_list.html", _project_list_context())


def project_detail(request, project_id):
    project = get_object_or_404(
        _project_detail_queryset(),
        pk=project_id,
    )
    return render(
        request,
        "tracker/project_detail.html",
        {
            "page_title": project.name,
            "project": project,
        },
    )


def project_create(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    source_page = request.POST.get("source_page", "project_list")
    form = ProjectForm(request.POST)
    if form.is_valid():
        form.save()
        if source_page == "dashboard":
            blank_form = ProjectForm()
            dashboard_context = _dashboard_context()
            return _render_mutation_response(
                request,
                [
                    (
                        "#dashboard-project-create-form-region",
                        "tracker/partials/project_form_panel.html",
                        _project_form_context(
                            blank_form,
                            "dashboard",
                            request.path,
                            "Add a project",
                            "Create project",
                        ),
                    ),
                    (
                        "#dashboard-stats-region",
                        "tracker/partials/dashboard_stats_panel.html",
                        dashboard_context,
                    ),
                    (
                        "#dashboard-recent-projects-region",
                        "tracker/partials/dashboard_recent_projects_panel.html",
                        dashboard_context,
                    ),
                ],
            )

        blank_form = ProjectForm()
        return _render_mutation_response(
            request,
            [
                (
                    "#project-create-form-region",
                    "tracker/partials/project_form_panel.html",
                    _project_form_context(
                        blank_form,
                        "project_list",
                        request.path,
                        "Add a project",
                        "Create project",
                    ),
                ),
                (
                    "#project-list-region",
                    "tracker/partials/project_list_panel.html",
                    _project_list_context(),
                ),
            ],
        )

    target_selector = (
        "#dashboard-project-create-form-region"
        if source_page == "dashboard"
        else "#project-create-form-region"
    )
    return _render_mutation_response(
        request,
        [
            (
                target_selector,
                "tracker/partials/project_form_panel.html",
                _project_form_context(
                    form,
                    source_page,
                    request.path,
                    "Add a project",
                    "Create project",
                ),
            )
        ],
        status=400,
    )


def project_update(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == "GET":
        return _render_mutation_response(
            request,
            [
                (
                    "#project-edit-form-region",
                    "tracker/partials/project_form_panel.html",
                    _project_form_context(
                        ProjectForm(instance=project),
                        "project_detail",
                        request.path,
                        f"Edit {project.name}",
                        "Save changes",
                    ),
                )
            ],
        )

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    form = ProjectForm(request.POST, instance=project)
    if form.is_valid():
        project = form.save()
        project = get_object_or_404(_project_detail_queryset(), pk=project.pk)
        return _render_mutation_response(
            request,
            [
                (
                    "#project-detail-region",
                    "tracker/partials/project_detail_panel.html",
                    {"project": project},
                ),
                (
                    "#project-edit-form-region",
                    "tracker/partials/project_edit_placeholder.html",
                    {},
                ),
            ],
        )

    return _render_mutation_response(
        request,
        [
            (
                "#project-edit-form-region",
                "tracker/partials/project_form_panel.html",
                _project_form_context(
                    form,
                    "project_detail",
                    request.path,
                    f"Edit {project.name}",
                    "Save changes",
                ),
            )
        ],
        status=400,
    )


def project_delete(request, project_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    project = get_object_or_404(Project, pk=project_id)
    source_page = request.POST.get("source_page", "project_detail")
    project_name = project.name
    project.delete()

    if source_page == "dashboard":
        dashboard_context = _dashboard_context()
        return _render_mutation_response(
            request,
            [
                (
                    "#dashboard-stats-region",
                    "tracker/partials/dashboard_stats_panel.html",
                    dashboard_context,
                ),
                (
                    "#dashboard-recent-projects-region",
                    "tracker/partials/dashboard_recent_projects_panel.html",
                    dashboard_context,
                ),
            ],
        )

    if source_page == "project_list":
        return _render_mutation_response(
            request,
            [
                (
                    "#project-list-region",
                    "tracker/partials/project_list_panel.html",
                    _project_list_context(),
                )
            ],
        )

    return _render_mutation_response(
        request,
        [
            (
                "#project-detail-region",
                "tracker/partials/project_deleted_panel.html",
                {"project_name": project_name},
            ),
            (
                "#project-edit-form-region",
                "tracker/partials/project_edit_placeholder.html",
                {},
            ),
        ],
    )


def tag_detail(request, tag_id):
    tag = get_object_or_404(
        Tag.objects.prefetch_related(
            Prefetch("projects", queryset=Project.objects.order_by("name")),
            Prefetch("tasks", queryset=Task.objects.select_related("project").order_by("due_date", "title")),
        ),
        pk=tag_id,
    )
    return render(
        request,
        "tracker/tag_detail.html",
        {
            "page_title": tag.name,
            "tag": tag,
        },
    )
