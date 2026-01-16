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
    CATEGORY_CHOICES = [
        ('language', 'Языки программирования'),
        ('database', 'Базы данных'),
        ('framework', 'Фреймворки'),
        ('devops', 'DevOps инструменты'),
        ('uiux', 'UI/UX'),
        ('testing', 'Тестирование'),
        ('mobile', 'Мобильная разработка'),
    ]

    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class ProjectTechnology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology = models.ForeignKey(Technology, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.project} — {self.technology}"