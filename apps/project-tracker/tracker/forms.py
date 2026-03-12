from django import forms

from .models import Project, Tag, Task


def _validate_choice(value: str, choices: list[tuple[str, str]], field_name: str) -> str:
    valid_values = {choice for choice, _label in choices}
    if value not in valid_values:
        raise forms.ValidationError(f"Choose a valid {field_name}.")
    return value


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["name", "description", "status", "created_date", "tags"]
        widgets = {
            "created_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_status(self) -> str:
        return _validate_choice(self.cleaned_data["status"], Project.STATUS_CHOICES, "status")


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["project", "title", "status", "priority", "due_date", "tags"]
        widgets = {
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_status(self) -> str:
        return _validate_choice(self.cleaned_data["status"], Task.STATUS_CHOICES, "status")

    def clean_priority(self) -> str:
        return _validate_choice(self.cleaned_data["priority"], Task.PRIORITY_CHOICES, "priority")


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name"]
