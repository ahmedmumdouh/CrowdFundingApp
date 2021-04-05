from django.db import models

# Create your models here.
#comments  -> users(FK) + projects(fk)
# class Comments (models.Model):   
#     pass
from  pusers.models import PUsers
from projects.models import Project

class Comments(models.Model):
    comment= models.CharField(max_length=200)
    status= models.CharField(max_length=20)
    Create_db =models.DateTimeField(auto_now_add=True)
    user_id= models.ForeignKey(PUsers, on_delete=models.CASCADE)
    project_id= models.ForeignKey(Project, on_delete=models.CASCADE)
