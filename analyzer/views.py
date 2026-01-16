from django.shortcuts import render, redirect
from .models import Project, Technology, ProjectTechnology
from .forms import ProjectTechnologyForm
from collections import Counter

def index(request):
    if request.method == "POST":
        form = ProjectTechnologyForm(request.POST)
        if form.is_valid():
            # Определяем проект
            project = form.cleaned_data["existing_project"]
            if not project:
                project_name = form.cleaned_data["new_project"]
                project, _ = Project.objects.get_or_create(name=project_name)

            # Определяем технологию
            technology = form.cleaned_data["existing_technology"]
            if not technology:
                tech_name = form.cleaned_data["new_technology"]
                category = form.cleaned_data["new_category"]
                technology, _ = Technology.objects.get_or_create(name=tech_name, defaults={"category": category})

            # Создаем связь
            ProjectTechnology.objects.get_or_create(project=project, technology=technology)

            return redirect("index")
    else:
        form = ProjectTechnologyForm()

    # Для таблицы популярности технологий
    project_techs = ProjectTechnology.objects.all()
    all_technologies = [pt.technology.name for pt in project_techs]
    technology_stats = dict(Counter(all_technologies))

    return render(request, "analyzer/index.html", {
        "form": form,
        "technology_stats": technology_stats
    })