from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    projects = models.ManyToManyField(Project, blank=True)

    def __str__(self):
        return self.user.username


class WorkLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    class Meta:
        unique_together = ("user", "project", "date")

    def __str__(self):
        return f"{self.user.username} - {self.project.name}: {self.hours}h"
