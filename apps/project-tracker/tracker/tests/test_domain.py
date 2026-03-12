from datetime import date

from django.core.exceptions import ValidationError
from django.test import TestCase

from tracker.forms import ProjectForm, TagForm, TaskForm
from tracker.models import Project, Tag, Task


class TrackerModelTests(TestCase):
    def test_project_and_task_support_tag_assignment(self):
        project = Project.objects.create(
            name="Launch site",
            description="Ship the marketing site.",
            status=Project.STATUS_ACTIVE,
        )
        task = Task.objects.create(
            project=project,
            title="Write copy",
            status=Task.STATUS_TODO,
            priority=Task.PRIORITY_HIGH,
        )
        tag = Tag.objects.create(name="marketing")

        project.tags.add(tag)
        task.tags.add(tag)

        self.assertQuerySetEqual(project.tags.order_by("name"), [tag], transform=lambda item: item)
        self.assertQuerySetEqual(task.tags.order_by("name"), [tag], transform=lambda item: item)

    def test_model_clean_rejects_invalid_enumerated_values(self):
        project = Project(
            name="Broken project",
            description="",
            status="invalid",
            created_date=date(2026, 3, 12),
        )
        task = Task(
            project=Project.objects.create(name="Base", description=""),
            title="Broken task",
            status="invalid",
            priority="urgent",
        )

        with self.assertRaises(ValidationError):
            project.full_clean()

        with self.assertRaises(ValidationError):
            task.full_clean()


class TrackerFormTests(TestCase):
    def test_project_form_accepts_locked_status_choices(self):
        form = ProjectForm(
            data={
                "name": "Roadmap",
                "description": "Quarterly plan",
                "status": Project.STATUS_COMPLETED,
                "created_date": "2026-03-12",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)

    def test_task_form_rejects_invalid_priority(self):
        project = Project.objects.create(name="Roadmap", description="")
        form = TaskForm(
            data={
                "project": project.pk,
                "title": "Rank backlog",
                "status": Task.STATUS_TODO,
                "priority": "urgent",
                "due_date": "2026-03-20",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("priority", form.errors)

    def test_tag_form_requires_name(self):
        form = TagForm(data={"name": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
