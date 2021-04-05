from django.db import models
from .project import Project


class Picture(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    image = models.ImageField(null=False, upload_to='project_images/')