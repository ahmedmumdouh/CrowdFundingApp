from django.shortcuts import render, get_object_or_404, redirect
from projects.models import Project, Picture, Tag,ProjectRate
from  comments.models import Comments
from .models import Donate
from  pusers.models import PUsers
from home.models import Category
from comments.forms import NewCommentForm
from .forms import NewDonateForm
import datetime
from django.http import JsonResponse


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
   
   
     
    all_comment=Comments.objects.all()
    current_user = request.user
    # username=PUsers.objects.filter(id=current_user.id)
    if request.method == 'POST':

        form=NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save
            # comment.save()
            comment=Comments.objects.create(

                comment=form.cleaned_data.get('comment'),
                # user_id=user
                 user_id_id=current_user.id ,
                 project_id_id=project_id
            )
            
            return redirect('viewProject',project_id=project_id)
    else:
        form=NewCommentForm

    
   
            

    return render(request,'projects/view.html',
    {
        'project':project,
        'images': images,
        'tags':tags,
        'comments':comments,
        'userObject':userObject,
        'category': category,
        'commentm':all_comment,
        'form':form,
       
    })


def update(request,project_id):
    if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        tags = Tag.objects.filter(project_id=project_id)
        tagValues = ''
        for tag in tags:
            tagValues += tag.tag + ' '
        category = Category.objects.all()
        return render(request,'projects/edit.html', {'project_dict':  project,'category':category, 'tags': tagValues})
    else:
        project = project = get_object_or_404(Project, id=project_id)
        project.title = request.POST.get('title')
        project.details = request.POST.get('details')
        project.category_id = request.POST.get('category')
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


def new_donate(request,projectId):
    projectObject=Project.objects.get(id=projectId)
    #user=User.objects.frist()
    all_donate=Donate.objects.all()
    current_user = request.user
    # username=PUsers.objects.filter(id=current_user.id)
    if request.method == 'POST':

        form=NewDonateForm(request.POST)
        if form.is_valid():
            # donate = form.save
            donate=Donate.objects.create(

                 value=form.cleaned_data.get('value'),
                # user_id=user
                 owner_id=current_user.id,
                 project_id=projectId
            )
            
            projectObject.total_donate +=form.cleaned_data.get('value')
            projectObject.save()
            
            return redirect('viewProject',project_id=projectId )
    else:
        form=NewDonateForm
    return render(request,'new_donate.html',{'donates':all_donate,'form':form})

# def new_rate(request):
#     projectObject=Project.objects.get(id=projectId)
#     # current_user = request.user
#     obj=ProjectRate.objects.filter(value=0).order_by("?").first()
#     context ={

#         'object':obj

#     }

    # if request.method == 'POST':

    #     # form=NewDonateForm(request.POST)
    #     # if form.is_valid():
    #     #     # donate = form.save
    #     rate=ProjectRate.objects.create(

    #             value= request.GET.POST('len'),
    #             owner_id=current_user.id,
    #             project_id=projectId
    #             )
            
            
            
    #     return redirect('viewProject',project_id=projectId )
   
    # return render(request,'new_rate.html',context)

def new_rate(request,projectId):
    # projectObject=Project.objects.get(id=projectId)
    current_user = request.user
    # if(not(ProjectRate.objects.filter(project_id=projectId ,owner_id=current_user.id))):
    rate=ProjectRate.objects.create(

            value=0,        
            owner_id=current_user.id,
            project_id=projectId
            )
    obj=Project.objects.filter(id=projectId).order_by("?").first()
    context ={

        'object':obj

    }
    return render(request,'new_rate.html',context)



def rate_project(request,projectId):
    current_user = request.user
    if request.method=='POST':
        val=request.POST.get('val')
        obj=ProjectRate.objects.get(project_id=projectId,owner_id=current_user.id)
        obj.value=val
        obj.save()
        return JsonResponse({'success':'true' ,'value':val }, safe=False)
    return   JsonResponse({'success':'false'})

def all_rates():
    allrates=ProjectRate.objects.all
    context={
    'allrates':allrates

    }
    return render('view',context)

