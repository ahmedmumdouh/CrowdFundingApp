from django.shortcuts import render
from projects.models import Project, Picture, Tag
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import datetime
from django.db.models.functions import Concat


def index(request):
    return render(request,'projects/index.html')

def Create(request):
    if request.method == "GET":
        return render(request, 'projects/add.html')
    else:
        project = Project.objects.create(
            title= request.POST.get('title'),
            details= request.POST.get('details'),
            category= request.POST.get('category'),
            total_target= request.POST.get('total_target'),
            start_date = request.POST.get('s_date'),
            end_date= request.POST.get('e_date')
        )
        uploadImages(request, Project.objects.last())
        return HttpResponse(Project.objects.last().id)

def uploadImages(dict, project):
    for file in dict.FILES.getlist('images'):
            uploaded_file_url = None
            myfile = file
            fs = FileSystemStorage()
            # f_name = Concat(,'_',myfile.name)
            # f_name = str(datetime.datetime.now()).
            # str(datetime.datetime.now()) + "_" + myfile.name
            # print(f_name)
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            image = Picture.objects.create(
                project_id =  project.id,
                image = file
            )

# def uploadImages(dict, project):
#      uploaded_file_url = None
#     for file in dict.FILES.getlist('images'):
#             myfile = file
#             fs = FileSystemStorage()
#             f_name = str(datetime.datetime.now()) + "_" + myfile.name
#             filename = fs.save(f_name, myfile)
#             uploaded_file_url = fs.url(filename)
#             image = Picture.objects.create(
#                 project_id =  Project.objects.last(),
#                 image = uploaded_file_url
#             )

def viewProject(request, project_id):
    return render(request,'view.html')
