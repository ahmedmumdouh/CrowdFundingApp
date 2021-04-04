from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=100,null=False,blank=False)
    details = models.CharField(max_length=255,null=False)
    # category = models.ForeignKey(cat) 
    category = models.CharField(max_length=100,null=False)
    total_target = models.DecimalField(max_digits=12,decimal_places=2,null=False)
    start_date = models.DateField(auto_now=False,auto_now_add=False,null=False)
    end_date = models.DateField(auto_now=False,auto_now_add=False,null=False)
    