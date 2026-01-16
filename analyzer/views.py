from django.shortcuts import render
from .models import ProjectTechnology  # твоя модель
from collections import Counter

def index(request):
    # Получаем все объекты из модели
    project_techs = ProjectTechnology.objects.all()

    # Создаем список технологий
    all_technologies = [pt.technology.name for pt in project_techs]  # pt.technology.name - строка

    # Считаем, сколько раз встречается каждая технология
    technology_stats = dict(Counter(all_technologies))  # преобразуем в словарь

    return render(request, 'analyzer/index.html', {
        'technology_stats': technology_stats
    })