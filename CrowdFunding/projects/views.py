from django.shortcuts import render,get_object_or_404
from projects.models import Project, Picture, Tag
from django.http import HttpResponse
import datetime


def index(request):
    projects = Project.objects.all()
    return render(request,'projects/index.html',{'projects':projects})

def Create(request):
    if request.method == "GET":
        return render(request, 'projects/add.html')
    else:
        print(request.POST.get('tags').split())
        project = Project.objects.create(
            title= request.POST.get('title'),
            details= request.POST.get('details'),
            category= request.POST.get('category'),
            total_target= request.POST.get('total_target'),
            start_date = request.POST.get('s_date'),
            end_date= request.POST.get('e_date')
        )
        uploadImages(request, Project.objects.last())
        uploadTags(request.POST.get('tags').split(),Project.objects.last())
        return render(request,'projects/index.html')


def uploadImages(dict, project):
    for file in dict.FILES.getlist('images'):
            file_name = str(file)
            indexofdot = file_name.index('.')
            ext = file_name[indexofdot:len(file_name)]
            file_name = file_name[:indexofdot]
            file.name = file_name + '_' + str(datetime.datetime.now()) + ext
            image = Picture.objects.create(
                project =  project,
                image = file
            )


def uploadTags(tags,project):
    for tag_name in tags:
        newTag = Tag.objects.create(
            project = project,
            tag = tag_name
        )


def show(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    images = Picture.objects.filter(project_id=project_id)
    tags = Tag.objects.filter(project_id=project_id)
    # delete image from project_images folder 
    # images[0].image.delete()
    print(tags)
    return render(request,'projects/view.html',
    {
        'project':project,
        'images': images,
        'tags':tags
    })
    # return HttpResponse(project_id)
