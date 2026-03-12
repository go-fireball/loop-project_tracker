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
        self.assertContains(response, "Write copy")
        self.assertContains(response, "Publish launch checklist")
        self.assertContains(response, "marketing")
        self.assertTemplateUsed(response, "tracker/project_detail.html")

    def test_tag_detail_route_renders_related_projects_and_tasks(self):
        response = self.client.get(reverse("tracker:tag_detail", args=[self.tag.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Tag: marketing")
        self.assertContains(response, "Launch site")
        self.assertContains(response, "Write copy")
        self.assertTemplateUsed(response, "tracker/tag_detail.html")
