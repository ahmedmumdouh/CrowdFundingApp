from django.db import models

# Create your models here.
#comments  -> users(FK) + projects(fk)
# class Comments (models.Model):   
#     pass

class Comments(models.Model):
    comment= models.CharField(max_length=200)
    status= models.CharField(max_length=20)
    user_id = models.IntegerField(max_length=20)
    project_id = models.IntegerField(max_length=20)
    Create_db =models.DateTimeField(auto_now_add=True)

    # user_id= models.ForeignKey(Users, on_delete=models.CASCADE)
    # project_id= models.ForeignKey(Project, on_delete=models.CASCADE)
