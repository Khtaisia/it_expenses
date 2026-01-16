from django.shortcuts import render
from django.http import JsonResponse
from .models import ProjectTechnology
from .forms import ProjectTechnologyForm
import requests
from collections import Counter

def index(request):
    form = ProjectTechnologyForm()

    # 🔹 Локальная статистика технологий
    all_techs = [pt.technology.name for pt in ProjectTechnology.objects.all()]
    tech_stats = dict(Counter(all_techs))

    return render(request, "analyzer/index.html", {
        "form": form,
        "tech_stats": tech_stats  # только локальные технологии
    })

def github_stats(request):
    """
    Возвращаем JSON с GitHub-популярностью только для технологий из локальной базы
    """
    local_techs = list(ProjectTechnology.objects.values_list("technology__name", flat=True).distinct())
    github_counts = {}
    headers = {"Accept": "application/vnd.github.v3+json"}

    for tech in local_techs:
        try:
            response = requests.get(
                f"https://api.github.com/search/repositories?q={tech}&sort=stars&order=desc",
                headers=headers,
                timeout=5
            )
            data = response.json()
            github_counts[tech] = data.get("total_count", 0)
        except Exception:
            github_counts[tech] = None  # если не получилось, показываем None (Загрузка…)

    return JsonResponse(github_counts)