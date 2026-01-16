from django import forms
from .models import Project, Technology, ProjectTechnology

class ProjectTechnologyForm(forms.Form):
    # Существующий проект
    existing_project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="Выбрать существующий проект"
    )
    # Новый проект
    new_project = forms.CharField(
        max_length=200,
        required=False,
        label="Или ввести новый проект"
    )
    # Существующая технология
    existing_technology = forms.ModelChoiceField(
        queryset=Technology.objects.all(),
        required=False,
        label="Выбрать существующую технологию"
    )
    # Новая технология
    new_technology = forms.CharField(
        max_length=100,
        required=False,
        label="Или ввести новую технологию"
    )
    # Категория для новой технологии
    new_category = forms.CharField(
        max_length=100,
        required=False,
        label="Категория новой технологии (язык, фреймворк, БД и т.д.)"
    )

    def clean(self):
        cleaned_data = super().clean()
        existing_project = cleaned_data.get("existing_project")
        new_project = cleaned_data.get("new_project")
        existing_technology = cleaned_data.get("existing_technology")
        new_technology = cleaned_data.get("new_technology")
        new_category = cleaned_data.get("new_category")

        if not (existing_project or new_project):
            raise forms.ValidationError("Нужно выбрать существующий проект или ввести новый.")

        if not (existing_technology or new_technology):
            raise forms.ValidationError("Нужно выбрать существующую технологию или ввести новую.")

        if new_technology and not new_category:
            raise forms.ValidationError("Если вводите новую технологию, укажите её категорию.")