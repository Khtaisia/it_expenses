from django.shortcuts import render
from .models import ProjectTechnology
import pandas as pd
import plotly.express as px
import plotly.io as pio

def index(request):
    # Получаем данные
    project_techs = ProjectTechnology.objects.all().values('technology__name')
    df = pd.DataFrame(list(project_techs))

    if not df.empty:
        # Считаем количество проектов по технологии
        technology_stats = df['technology__name'].value_counts().to_dict()

        # Создаём график
        fig = px.bar(
            x=list(technology_stats.keys()),
            y=list(technology_stats.values()),
            labels={'x':'Технология', 'y':'Количество проектов'},
            title='Популярность технологий в проектах'
        )

        # Преобразуем график в HTML
        graph_html = pio.to_html(fig, full_html=False)
    else:
        technology_stats = {}
        graph_html = "<p>Нет данных для построения графика</p>"

    return render(request, 'analyzer/index.html', {
        'technology_stats': technology_stats,
        'graph_html': graph_html
    })