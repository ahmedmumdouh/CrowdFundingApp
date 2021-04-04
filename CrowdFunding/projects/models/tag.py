from django.db import models
from .project import Project


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, null=False)
    tag = models.CharField(max_length=100, null=False)