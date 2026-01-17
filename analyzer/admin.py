from django.contrib import admin
from .models import Project, Technology, ProjectTechnology

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    search_fields = ('name', 'category')
    list_filter = ('category',)  # добавлен фильтр по категории

@admin.register(ProjectTechnology)
class ProjectTechnologyAdmin(admin.ModelAdmin):
    list_display = ('project', 'technology')
    search_fields = ('project__name', 'technology__name')
    list_filter = ('project', 'technology')  # добавлены фильтры