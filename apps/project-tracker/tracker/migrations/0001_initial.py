import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("active", "Active"), ("completed", "Completed"), ("archived", "Archived")], default="active", max_length=20)),
                ("created_date", models.DateField(default=django.utils.timezone.localdate)),
                ("tags", models.ManyToManyField(blank=True, related_name="projects", to="tracker.tag")),
            ],
            options={
                "ordering": ["name", "-created_date"],
            },
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("status", models.CharField(choices=[("todo", "To Do"), ("in_progress", "In Progress"), ("done", "Done")], default="todo", max_length=20)),
                ("priority", models.CharField(choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")], default="medium", max_length=20)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("project", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="tracker.project")),
                ("tags", models.ManyToManyField(blank=True, related_name="tasks", to="tracker.tag")),
            ],
            options={
                "ordering": ["due_date", "title"],
            },
        ),
    ]
