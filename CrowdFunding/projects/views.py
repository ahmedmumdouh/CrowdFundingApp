from django.shortcuts import render, get_object_or_404, redirect
from projects.models import Project, Picture, Tag
from  comments.models import Comments
from  pusers.models import PUsers
from home.models import Category
import datetime


def index(request):
    projects = Project.objects.select_related('category')
    return render(request,'projects/index.html',{'projects':projects})

def Create(request):
    
    if request.method == "GET":
        project = Project(None)
        category = Category.objects.all()
        return render(request, 'projects/add.html',{'new_project':project,'category':category})
    else:
        project = Project(
            title= request.POST.get('title'),
            details= request.POST.get('details'),
            category_id = request.POST.get('category'),
            total_target= request.POST.get('total_target'),
            start_date = request.POST.get('s_date'),
            end_date= request.POST.get('e_date'),
            owner_id = request.user.id
        )
        if project.clean():
            project.save()
            uploadImages(request, Project.objects.last())
            uploadTags(request.POST.get('tags').split(),Project.objects.last())
            return redirect('projects')
        else:
            category = Category.objects.all()
            return render(request, 'projects/add.html',{'new_project':project,'category':category})


def uploadImages(images, project):
    for file in images.FILES.getlist('images'):
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
    comments=Comments.objects.filter(project_id=project_id)
    category = Category.objects.get(id=project.category_id)
    current_user = request.user
    userObject=PUsers.objects.get(id=current_user.id)
    # delete image from project_images folder 
    # images[0].image.delete()
    print(tags)
    return render(request,'projects/view.html',
    {
        'project':project,
        'images': images,
        'tags':tags,
        'comments':comments,
        'userObject':userObject,
        'category': category
    })


def update(request,project_id):
    if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        tags = Tag.objects.filter(project_id=project_id)
        tagValues = ''
        for tag in tags:
            tagValues += tag.tag + ' '
        return render(request,'projects/edit.html', {'project_dict':  project, 'tags': tagValues})
    else:
        project = project = get_object_or_404(Project, id=project_id)
        project.title = request.POST.get('title')
        project.details = request.POST.get('details')
        project.category = request.POST.get('category')
        project.total_target = request.POST.get('total_target')
        project.start_date = request.POST.get('s_date')
        project.end_date = request.POST.get('e_date')
        project.save()
        tags = Tag.objects.filter(project_id=project_id)
        tagValues = ''
        for tag in tags:
            tagValues += tag.tag + ' '
        
        # if tags not changed
        if tagValues ==  request.POST.get('tags'):
            # if upload new images
            if request.FILES:
                # update images only here
                deleteOldImages(project)
                uploadImages(request,project)
        else:
            # if images and tags changed 
            if request.FILES:
                #update image and tags here
                deleteOldImages(project)
                uploadImages(request,project)
                deleteOldTags(tags)
                uploadTags(request.POST.get('tags').split(),project)
            else:
                # if tags only changed 
                deleteOldTags(tags)
                uploadTags(request.POST.get('tags').split(),project)
        return redirect('projects')


def deleteOldImages(project):
    images = Picture.objects.filter(project_id=project.id)
    for image in images:
        image.image.delete()
        image.delete()


def deleteOldTags(tags):
    for tag in tags:
        tag.delete()


def deleteProject(request, project_id):
    project = get_object_or_404(Project, id= project_id)
    deleteOldImages(project)
    project.delete()
    return redirect('projects')


