# from .models import Picture,Project,Tag,Donate
from django.db import models
from  pusers.models import PUsers
# from   projects.models import Project
from django.core.exceptions import ValidationError
import datetime
from home.models import Category


class Project(models.Model):
    owner = models.ForeignKey(PUsers, on_delete = models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete= models.CASCADE)
    total_target = models.DecimalField(max_digits=12,decimal_places=2)
    start_date = models.DateField(auto_now=False,auto_now_add=False)
    end_date = models.DateField(auto_now=False,auto_now_add=False)
    
    errors = {}
    def clean(self):
        valid = True
        start_date = self.start_date
        end_date = self.end_date
        self.errors = {}
        if end_date == '' or start_date == '':
            self.errors['date'] = 'date is required'
            valid = False
        elif start_date < str(datetime.date.today()):
            self.errors['date'] = 'invalid date'
            valid = False
        elif end_date == start_date:
            self.errors['date'] = 'invalid date'
            valid = False
        elif end_date < start_date:
            self.errors['date'] = 'invalid date'
            # 'End date should be greater than start date.'
            valid = False
        elif end_date == datetime.date.today():
            self.errors['date'] = 'invalid date'
            valid = False
        if self.title == '':
            self.errors['title'] = 'title is required'
            valid = False
        if self.details == '':
            self.errors['details'] = 'details is required'
            valid = False
        if self.total_target == '':
            self.errors['total_target'] = 'total_target is required'
            valid = False
        return valid


class Picture(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    image = models.ImageField(null=False, upload_to='project_images/')

  


class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE, null=False)
    tag = models.CharField(max_length=100, null=False)

    def clean(self):
        valid = True
        if self.tag == '':
            valid = False
        return valid


class Donate(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    owner = models.ForeignKey(PUsers, on_delete = models.CASCADE)
    value=models.DecimalField(max_digits=12,decimal_places=2)

class ProjectRate(models.Model):
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    owner = models.ForeignKey(PUsers, on_delete = models.CASCADE)
    value=models.DecimalField(max_digits=12,decimal_places=2)