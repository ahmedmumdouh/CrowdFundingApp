from django.db import connection
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import datetime
from .models import Category
from django.http import JsonResponse
from django.http import HttpResponse

from .forms import NewCategoryForm
from projects.models import Project
from projects.models import Picture
from projects.models import Tag
from projects.models import ProjectRate
from django.db.models import Avg

import json




# Create your views here.

def index(request):
<<<<<<< HEAD

   
=======
    if request.method=='GET':
         all_category= Category.objects.all()
        latest_projects = Project.objects.order_by('-start_date')[:5]
        admin_projects = Project.objects.order_by('-id')[:5]

        # highestRating = cursor.execute('select projects_project.title, sum(rate)as sumRating from projects_project join projects_projectrate where projects_project.id == projects_projectrate.project_id GROUP by projects_projectrate.project_id order by sumRating DESC limit 5;')
        #  Project.objects.select_related('category')
        #  qqq = Project.objects.raw('SELECT  id,title , sum(rate)as sumRating FROM projects_project JOIN projects_projectrate   WHERE id = project_id' )
        #qqq = ProjectRate.objects.group_by('project_id').count()
        highestRating =ProjectRate.objects.values('project_id').annotate(average_rating=Avg('value')).order_by('-average_rating')[:2]


        images = []
        imagesrate = []
        imagesadmin= []



        for project in latest_projects:
            images.append(Picture.objects.filter(project_id=project.id).first())

        for project in highestRating:
            imagesrate.append(Picture.objects.filter(project_id=project['project_id']).first())

        for project in admin_projects:
            imagesadmin.append(Picture.objects.filter(project_id=project.id).first())

        context = {
            'all_category': all_category,
            'latest_projects': latest_projects,
            'highestRating': highestRating,
            'images': images,
            'imagesrate': imagesrate,
            'admin_projects': admin_projects,
            'imagesadmin': imagesadmin,
        }
        return  render(request, 'home/index.html',context )
    elif request.method == 'POST':
            val = request.POST.get('val')
            print(val)
            projectcat=Project.objects.filter(category_id=val)
             
            
            print(projectcat)
            # context = {
            # 'obj':projectcat
            #  }
        #    JsonResponse(dict(genres=list(projectcat))
            json_result=[]
            for cat in projectcat:
                img=Picture.objects.get(project_id=cat.id)
                print(img.image)
                image_path=str(img.image)
                total_target=str(cat.total_target)
                print(image_path)
                json_object=dict(title=cat.title,total_target=total_target,image=image_path,project_id=cat.id)
                json_result.append(json_object)
            return JsonResponse({'success': 'true', 'value':json.dumps(json_result)}, safe=False)
            # return  render(request , 'home/index.html',{'projectcat':projectcat} )
    # else:
    #     return JsonResponse({'success': 'false'})
    
    
   
    

def new_category(request): 
#    user=User.objects.frist()
    all_category=Category.objects.all()
    if request.method == 'POST':
        form=NewCategoryForm(request.POST)
        if form.is_valid():
            category= form.save
            # comment.save()
            category=Category.objects.create(
                name=form.cleaned_data.get('name')               
            )
            return redirect('show')
    else:
        form=NewCategoryForm() 
    return render(request,'category/new_category.html',{'category':all_category,'form':form})


def show(request):
     all_category= Category.objects.all()
     return render(request,'category/show.html',{'category':all_category})


def my_projects(request):
    my_projects = Project.objects.select_related('owner').filter(owner_id=request.user.id)
    # images = Picture.objects.filter(project_id=project_id)
    # tags = Tag.objects.filter(project_id=project_id)
    # comments=Comments.objects.filter(project_id=project_id)
    # category = Category.objects.get(id=project.category_id)
    # current_user = request.user
    # userObject=PUsers.objects.get(id=current_user.id)
    return render(request,'my_projects/show.html',{'my_projects':my_projects})

def searchName(request):

    if request.method == 'POST':
        result = request.POST.get('search_name')

        results = Project.objects.filter(title=result)
        context = {
            "results": results,
            "yoursearch": result
        }
        return render(request, 'home/searchResults.html', context)

def searchTag(request):

    if request.method == 'POST':
        result = request.POST.get('search_tag')
        resultss = Tag.objects.filter(tag=result)
      #  results = Project.objects.filter(tag=resultss)
        context = {
            "results": resultss,
            "yoursearch": result
        }
        return render(request, 'home/searchResultsTag.html', context)

# def categoryprojects(request,category_id):
#     #  if request.method == 'GET':
#     #     projectObject = Project.objects.get(id=project_id)
#     if request.method == 'POST':
#         val = request.POST.get('id')
#         obj =Project.objects.filter(category_id=val)
#         context={
#             'obj':obj
#         }
#         return JsonResponse({'success': 'true', 'value': val}, safe=False)
#     else:
#         return JsonResponse({'success': 'false'})
#     return render(request, 'home/index.html', context)

