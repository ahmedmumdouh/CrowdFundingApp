from django.db import models


# Create your models here.
# comments_report   + projects_reports   -->  users(FK) + comments(fk) + projects(fk)   Report_comments   Report_projects

class ReportComment(models.Model):
    title= models.CharField(max_length=100, default="Untitiled")
    body_comment = models.TextField(max_length=4000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title, self.body_comment


class ReportProject(models.Model):
    title = models.CharField(max_length=100, default="Untitiled")
    body_project = models.TextField(max_length=4000, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title, self.body_project

    #  user = models.ForeignKey('Users', null=True,
    #                   on_delete=models.CASCADE)
    # project = models.ForeignKey(
    #      'Project', null=True, on_delete=models.CASCADE)
    #   comment = models.ForeignKey(
    #      'Comment', null=True, on_delete=models.CASCADE)
    # user_id = models.IntegerField(blank=True, null=True)
    # project_id = models.IntegerField(blank=True, null=True)