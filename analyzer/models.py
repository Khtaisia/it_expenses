from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название проекта"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание проекта"
    )

    def __str__(self):
        return self.name


class Technology(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Название технологии"
    )
    category = models.CharField(
        max_length=100,
        verbose_name="Категория (язык, фреймворк, БД и т.д.)"
    )

    def __str__(self):
        return self.name


class ProjectTechnology(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE
    )
    technology = models.ForeignKey(
        Technology,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.project} — {self.technology}"