from django import forms
from .models import Project, Technology

class ProjectTechnologyForm(forms.Form):
    existing_project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        required=False,
        label="Выбрать существующий проект"
    )
    new_project = forms.CharField(
        max_length=200,
        required=False,
        label="Или ввести новый проект"
    )


    TECH_CATEGORIES = {
        "Языки программирования": ["Python", "JavaScript", "Java", "C#", "Go"],
        "Фреймворки": ["Django", "Flask", "React", "Angular", "Vue"],
        "Базы данных": ["PostgreSQL", "MySQL", "SQLite", "MongoDB", "Redis"],
        "Инструменты": ["Git", "Docker", "VS Code", "Postman", "Jira"],
        "DevOps": ["Jenkins", "GitLab CI", "Kubernetes", "Ansible", "Terraform"],
        "UI/UX": ["Figma", "Adobe XD", "Sketch", "InVision", "Balsamiq"],
        "Безопасность": ["OAuth", "JWT", "SSL", "OpenSSL", "HashiCorp Vault"],
    }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for category, tech_list in self.TECH_CATEGORIES.items():
            self.fields[category] = forms.MultipleChoiceField(
                choices=[(t, t) for t in tech_list],
                widget=forms.CheckboxSelectMultiple,
                required=False,
                label=category
            )


    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get("existing_project") and not cleaned_data.get("new_project"):
            raise forms.ValidationError("Выберите существующий проект или введите новый.")
        any_tech_selected = any(cleaned_data.get(cat) for cat in self.TECH_CATEGORIES)
        if not any_tech_selected:
            raise forms.ValidationError("Выберите хотя бы одну технологию.")