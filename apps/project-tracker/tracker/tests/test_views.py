from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from tracker.models import Project, Tag, Task


class TrackerViewTests(TestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Launch site",
            description="Ship the marketing site.",
            status=Project.STATUS_ACTIVE,
        )
        self.other_project = Project.objects.create(
            name="Archive docs",
            description="Tidy older project notes.",
            status=Project.STATUS_ARCHIVED,
        )
        self.tag = Tag.objects.create(name="marketing")
        self.project.tags.add(self.tag)

        self.task = Task.objects.create(
            project=self.project,
            title="Write copy",
            status=Task.STATUS_IN_PROGRESS,
            priority=Task.PRIORITY_HIGH,
            due_date=timezone.localdate() - timedelta(days=1),
        )
        self.task.tags.add(self.tag)
        Task.objects.create(
            project=self.project,
            title="Publish launch checklist",
            status=Task.STATUS_DONE,
            priority=Task.PRIORITY_MEDIUM,
        )
        Task.objects.create(
            project=self.other_project,
            title="Audit legacy docs",
            status=Task.STATUS_TODO,
            priority=Task.PRIORITY_LOW,
        )

    def test_dashboard_route_renders_live_aggregates(self):
        response = self.client.get(reverse("tracker:dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dashboard")
        self.assertContains(response, "Total projects")
        self.assertContains(response, "2")
        self.assertContains(response, "In Progress tasks")
        self.assertContains(response, "Overdue tasks")
        self.assertContains(response, "Launch site")
        self.assertTemplateUsed(response, "tracker/dashboard.html")

    def test_project_list_route_renders_projects_and_metadata(self):
        response = self.client.get(reverse("tracker:project_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Launch site")
        self.assertContains(response, "Archive docs")
        self.assertContains(response, "marketing")
        self.assertContains(response, "open tasks")
        self.assertTemplateUsed(response, "tracker/project_list.html")

    def test_project_detail_route_renders_project_tasks_and_tags(self):
        response = self.client.get(reverse("tracker:project_detail", args=[self.project.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Launch site")
        self.assertContains(response, "2 tasks")
        self.assertContains(response, "Write copy")
        self.assertContains(response, "Publish launch checklist")
        self.assertContains(response, "marketing")
        self.assertTemplateUsed(response, "tracker/project_detail.html")

    def test_tag_detail_route_renders_related_projects_and_tasks(self):
        response = self.client.get(reverse("tracker:tag_detail", args=[self.tag.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tag management")
        self.assertContains(response, "Tag: marketing")
        self.assertContains(response, "Launch site")
        self.assertContains(response, "Write copy")
        self.assertTemplateUsed(response, "tracker/tag_detail.html")

    def test_tag_list_route_renders_management_surface_without_selection(self):
        response = self.client.get(reverse("tracker:tag_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tag management")
        self.assertContains(response, "Select a tag")
        self.assertContains(response, "marketing")
        self.assertTemplateUsed(response, "tracker/tag_detail.html")

    def test_tag_detail_ajax_returns_swap_targets_for_management_surface(self):
        response = self.client.get(
            reverse("tracker:tag_detail", args=[self.tag.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#tag-list-region"')
        self.assertContains(response, 'data-swap-target="#tag-detail-region"')
        self.assertContains(response, 'data-swap-target="#tag-edit-form-region"')
        self.assertContains(response, "Tag: marketing")
        self.assertContains(response, "list-card-active")

    def test_project_create_returns_partial_updates_for_project_list(self):
        response = self.client.post(
            reverse("tracker:project_create"),
            {
                "source_page": "project_list",
                "name": "Client portal",
                "description": "Build the account portal.",
                "status": Project.STATUS_ACTIVE,
                "created_date": timezone.localdate().isoformat(),
                "tags": [self.tag.id],
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-create-form-region"')
        self.assertContains(response, 'data-swap-target="#project-list-region"')
        self.assertTrue(Project.objects.filter(name="Client portal").exists())

    def test_project_create_invalid_returns_inline_errors(self):
        response = self.client.post(
            reverse("tracker:project_create"),
            {
                "source_page": "dashboard",
                "name": "",
                "description": "Missing name should fail.",
                "status": Project.STATUS_ACTIVE,
                "created_date": timezone.localdate().isoformat(),
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'data-swap-target="#dashboard-project-create-form-region"', status_code=400)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_project_update_get_returns_edit_form_partial(self):
        response = self.client.get(
            reverse("tracker:project_update", args=[self.project.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-edit-form-region"')
        self.assertContains(response, "Save changes")
        self.assertContains(response, "Launch site")

    def test_project_update_post_returns_updated_detail_partial(self):
        response = self.client.post(
            reverse("tracker:project_update", args=[self.project.id]),
            {
                "source_page": "project_detail",
                "name": "Launch site v2",
                "description": "Ship the refreshed marketing site.",
                "status": Project.STATUS_COMPLETED,
                "created_date": self.project.created_date.isoformat(),
                "tags": [self.tag.id],
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.project.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.project.name, "Launch site v2")
        self.assertEqual(self.project.status, Project.STATUS_COMPLETED)
        self.assertContains(response, 'data-swap-target="#project-detail-region"')
        self.assertContains(response, "Launch site v2")
        self.assertContains(response, "Completed")

    def test_project_update_invalid_returns_inline_errors(self):
        response = self.client.post(
            reverse("tracker:project_update", args=[self.project.id]),
            {
                "source_page": "project_detail",
                "name": "",
                "description": "Ship the refreshed marketing site.",
                "status": Project.STATUS_COMPLETED,
                "created_date": self.project.created_date.isoformat(),
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.project.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.project.name, "Launch site")
        self.assertContains(response, 'data-swap-target="#project-edit-form-region"', status_code=400)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_project_delete_from_detail_returns_deleted_panel(self):
        response = self.client.post(
            reverse("tracker:project_delete", args=[self.project.id]),
            {"source_page": "project_detail"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-detail-region"')
        self.assertContains(response, 'data-swap-target="#task-create-form-region"')
        self.assertContains(response, 'data-swap-target="#task-edit-form-region"')
        self.assertContains(response, 'data-swap-target="#task-list-region"')
        self.assertContains(response, "Project deleted")
        self.assertNotContains(response, "Create task")
        self.assertNotContains(response, "Write copy")
        self.assertFalse(Project.objects.filter(id=self.project.id).exists())

    def test_project_delete_from_dashboard_updates_recent_projects_partial(self):
        response = self.client.post(
            reverse("tracker:project_delete", args=[self.project.id]),
            {"source_page": "dashboard"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#dashboard-stats-region"')
        self.assertContains(response, 'data-swap-target="#dashboard-recent-projects-region"')
        self.assertNotContains(response, "Launch site")

    def test_project_delete_from_project_list_returns_refreshed_list_region(self):
        response = self.client.post(
            reverse("tracker:project_delete", args=[self.project.id]),
            {"source_page": "project_list"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-list-region"')
        self.assertNotContains(response, "Launch site")
        self.assertContains(response, "Archive docs")

    def test_task_create_success_from_project_detail_returns_updated_regions(self):
        response = self.client.post(
            reverse("tracker:task_create", args=[self.project.id]),
            {
                "title": "Ship assets",
                "status": Task.STATUS_TODO,
                "priority": Task.PRIORITY_MEDIUM,
                "due_date": timezone.localdate().isoformat(),
                "tags": [self.tag.id],
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-detail-region"')
        self.assertContains(response, 'data-swap-target="#task-create-form-region"')
        self.assertContains(response, 'data-swap-target="#task-list-region"')
        self.assertContains(response, "3 tasks")
        self.assertContains(response, "Ship assets")
        self.assertTrue(Task.objects.filter(project=self.project, title="Ship assets").exists())

    def test_task_create_invalid_returns_inline_errors(self):
        response = self.client.post(
            reverse("tracker:task_create", args=[self.project.id]),
            {
                "title": "",
                "status": Task.STATUS_TODO,
                "priority": Task.PRIORITY_MEDIUM,
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'data-swap-target="#task-create-form-region"', status_code=400)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_task_update_get_returns_edit_form_partial(self):
        response = self.client.get(
            reverse("tracker:task_update", args=[self.project.id, self.task.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#task-edit-form-region"')
        self.assertContains(response, "Save task")
        self.assertContains(response, "Write copy")

    def test_task_update_post_returns_updated_task_regions(self):
        response = self.client.post(
            reverse("tracker:task_update", args=[self.project.id, self.task.id]),
            {
                "title": "Write launch copy",
                "status": Task.STATUS_DONE,
                "priority": Task.PRIORITY_LOW,
                "due_date": timezone.localdate().isoformat(),
                "tags": [self.tag.id],
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.task.title, "Write launch copy")
        self.assertEqual(self.task.status, Task.STATUS_DONE)
        self.assertContains(response, 'data-swap-target="#project-detail-region"')
        self.assertContains(response, 'data-swap-target="#task-list-region"')
        self.assertContains(response, "Write launch copy")
        self.assertContains(response, "Done")

    def test_task_update_invalid_returns_inline_errors(self):
        response = self.client.post(
            reverse("tracker:task_update", args=[self.project.id, self.task.id]),
            {
                "title": "",
                "status": Task.STATUS_DONE,
                "priority": Task.PRIORITY_LOW,
                "due_date": timezone.localdate().isoformat(),
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.task.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.task.title, "Write copy")
        self.assertContains(response, 'data-swap-target="#task-edit-form-region"', status_code=400)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_task_delete_returns_refreshed_task_list_and_summary(self):
        response = self.client.post(
            reverse("tracker:task_delete", args=[self.project.id, self.task.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#project-detail-region"')
        self.assertContains(response, 'data-swap-target="#task-list-region"')
        self.assertContains(response, "1 tasks")
        self.assertNotContains(response, "Write copy")
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_tag_create_success_returns_updated_management_regions(self):
        response = self.client.post(
            reverse("tracker:tag_create"),
            {"name": "backend"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#tag-create-form-region"')
        self.assertContains(response, 'data-swap-target="#tag-list-region"')
        self.assertContains(response, 'data-swap-target="#tag-detail-region"')
        self.assertContains(response, 'data-swap-target="#tag-edit-form-region"')
        self.assertContains(response, "Tag: backend")
        self.assertTrue(Tag.objects.filter(name="backend").exists())

    def test_tag_create_invalid_returns_inline_errors(self):
        response = self.client.post(
            reverse("tracker:tag_create"),
            {"name": ""},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, 'data-swap-target="#tag-create-form-region"', status_code=400)
        self.assertContains(response, "This field is required.", status_code=400)

    def test_tag_update_get_returns_edit_form_partial(self):
        response = self.client.get(
            reverse("tracker:tag_update", args=[self.tag.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#tag-edit-form-region"')
        self.assertContains(response, "Edit marketing")
        self.assertContains(response, "Save tag")
        self.assertContains(response, "Cancel")

    def test_tag_update_post_returns_updated_tag_regions(self):
        response = self.client.post(
            reverse("tracker:tag_update", args=[self.tag.id]),
            {"name": "growth"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.tag.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.tag.name, "growth")
        self.assertContains(response, 'data-swap-target="#tag-list-region"')
        self.assertContains(response, 'data-swap-target="#tag-detail-region"')
        self.assertContains(response, "Tag: growth")
        self.assertContains(response, "Launch site")

    def test_tag_update_invalid_returns_inline_errors(self):
        duplicate_tag = Tag.objects.create(name="growth")
        response = self.client.post(
            reverse("tracker:tag_update", args=[self.tag.id]),
            {"name": duplicate_tag.name},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.tag.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.tag.name, "marketing")
        self.assertContains(response, 'data-swap-target="#tag-edit-form-region"', status_code=400)
        self.assertContains(response, "already exists", status_code=400)

    def test_tag_delete_returns_refreshed_regions_and_clears_selection(self):
        response = self.client.post(
            reverse("tracker:tag_delete", args=[self.tag.id]),
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data-swap-target="#tag-create-form-region"')
        self.assertContains(response, 'data-swap-target="#tag-list-region"')
        self.assertContains(response, 'data-swap-target="#tag-detail-region"')
        self.assertContains(response, 'data-swap-target="#tag-edit-form-region"')
        self.assertContains(response, "Deleted tag: marketing")
        self.assertFalse(Tag.objects.filter(id=self.tag.id).exists())

    def test_mutation_routes_reject_disallowed_methods(self):
        response = self.client.get(reverse("tracker:project_create"))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse("tracker:project_update", args=[self.project.id]))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse("tracker:task_create", args=[self.project.id]))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse("tracker:task_update", args=[self.project.id, self.task.id]))
        self.assertEqual(response.status_code, 405)

        response = self.client.get(reverse("tracker:tag_create"))
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse("tracker:tag_update", args=[self.tag.id]))
        self.assertEqual(response.status_code, 405)
