from django.db import models
from  pusers.models import PUsers
from projects.models import Project
from comments.models import Comments


# Create your models here.
# comments_report   + projects_reports   -->  users(FK) + comments(fk) + projects(fk)   Report_comments   Report_projects

class ReportComment(models.Model):
    title= models.CharField(max_length=100, default="Untitiled")
    body_comment = models.TextField(max_length=4000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(PUsers, null=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comments, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title, self.body_comment


class ReportProject(models.Model):
    title = models.CharField(max_length=100, default="Untitiled")
    body_project = models.TextField(max_length=4000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(PUsers, null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.title, self.body_project

 
  

         
    # user_id = models.IntegerField(blank=True, null=True)
    # project_id = models.IntegerField(blank=True, null=True)