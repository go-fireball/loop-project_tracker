from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Project(models.Model):
    STATUS_ACTIVE = "active"
    STATUS_COMPLETED = "completed"
    STATUS_ARCHIVED = "archived"
    STATUS_CHOICES = [
        (STATUS_ACTIVE, "Active"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
    )
    created_date = models.DateField(default=timezone.localdate)
    tags = models.ManyToManyField(Tag, blank=True, related_name="projects")

    class Meta:
        ordering = ["name", "-created_date"]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        super().clean()
        valid_statuses = {choice for choice, _label in self.STATUS_CHOICES}
        if self.status not in valid_statuses:
            raise ValidationError({"status": "Choose a valid status."})


class Task(models.Model):
    STATUS_TODO = "todo"
    STATUS_IN_PROGRESS = "in_progress"
    STATUS_DONE = "done"
    STATUS_CHOICES = [
        (STATUS_TODO, "To Do"),
        (STATUS_IN_PROGRESS, "In Progress"),
        (STATUS_DONE, "Done"),
    ]

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_TODO,
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM,
    )
    due_date = models.DateField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="tasks")

    class Meta:
        ordering = ["due_date", "title"]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        super().clean()
        valid_statuses = {choice for choice, _label in self.STATUS_CHOICES}
        valid_priorities = {choice for choice, _label in self.PRIORITY_CHOICES}
        errors = {}
        if self.status not in valid_statuses:
            errors["status"] = "Choose a valid status."
        if self.priority not in valid_priorities:
            errors["priority"] = "Choose a valid priority."
        if errors:
            raise ValidationError(errors)
