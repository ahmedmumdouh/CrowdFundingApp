from django.db import models

# Create your models here.
#category

class Category(models.Model):
    name= models.CharField(max_length=200)
    status= models.CharField(max_length=20)
    Create_db =models.DateTimeField(auto_now_add=True)