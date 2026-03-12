from django.contrib import admin

from .models import Project, Tag, Task


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "created_date")
    list_filter = ("status", "created_date", "tags")
    search_fields = ("name", "description")
    filter_horizontal = ("tags",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "due_date")
    list_filter = ("status", "priority", "due_date", "project", "tags")
    search_fields = ("title", "project__name")
    autocomplete_fields = ("project",)
    filter_horizontal = ("tags",)
