from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Project, Technology, ProjectTechnology
from .forms import ProjectTechnologyForm
import requests
from django.db.models import Count


def index(request):
    # ---------- СОХРАНЕНИЕ ДАННЫХ ----------
    if request.method == "POST":
        form = ProjectTechnologyForm(request.POST)
        if form.is_valid():
            # 1️⃣ Определяем проект
            project = form.cleaned_data["existing_project"]
            new_project_name = form.cleaned_data["new_project"]

            if not project and new_project_name:
                project, created = Project.objects.get_or_create(
                    name=new_project_name
                )

            # 2️⃣ Сохраняем выбранные технологии
            for category in form.TECH_CATEGORIES:
                selected_techs = form.cleaned_data.get(category)
                if selected_techs:
                    for tech_name in selected_techs:
                        tech_obj, _ = Technology.objects.get_or_create(
                            name=tech_name
                        )
                        ProjectTechnology.objects.get_or_create(
                            project=project,
                            technology=tech_obj
                        )

            # redirect — good practice
            return redirect("index")
    else:
        form = ProjectTechnologyForm()

    # ---------- ФИЛЬТРАЦИЯ ----------
    selected_project_id = request.GET.get("project")

    project_tech_qs = ProjectTechnology.objects.all()

    if selected_project_id:
        project_tech_qs = project_tech_qs.filter(
            project_id=selected_project_id
        )

    # ---------- АГРЕГАЦИЯ + СОРТИРОВКА ----------
    tech_stats_qs = (
        project_tech_qs
        .values("technology__name")
        .annotate(count=Count("technology"))
        .order_by("-count")  # сортировка по популярности
    )

    tech_stats = {
        item["technology__name"]: item["count"]
        for item in tech_stats_qs
    }

    return render(
        request,
        "analyzer/index.html",
        {
            "form": form,
            "tech_stats": tech_stats,
            "projects": Project.objects.all(),
            "selected_project_id": selected_project_id,
        }
    )


def github_stats(request):
    """
    Возвращаем JSON с GitHub-популярностью
    только для технологий из локальной базы
    """
    local_techs = list(
        ProjectTechnology.objects
        .values_list("technology__name", flat=True)
        .distinct()
    )

    github_counts = {}
    headers = {"Accept": "application/vnd.github.v3+json"}

    for tech in local_techs:
        try:
            response = requests.get(
                f"https://api.github.com/search/repositories?q={tech}&sort=stars&order=desc",
                headers=headers,
                timeout=5,
            )
            data = response.json()
            github_counts[tech] = data.get("total_count", 0)
        except Exception:
            github_counts[tech] = None

    return JsonResponse(github_counts)