from django.db import models
from .project import Project
from  pusers.models import PUsers


class ProjectRate(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    owner = models.ForeignKey(PUsers, on_delete = models.CASCADE)
    value=models.DecimalField(max_digits=12,decimal_places=2)