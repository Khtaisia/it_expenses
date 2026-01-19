from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/github-stats/", views.github_stats, name="github_stats"),
    path("api/category-stats/", views.categories_stats_api, name="category_stats_api"),
]