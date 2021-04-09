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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def index(request):
    if request.method=='GET':
        all_category= Category.objects.all()
        latest_projects = Project.objects.order_by('-start_date')[:5]
        admin_projects = Project.objects.order_by('-id')[:5]
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
           
            if(Category.objects.filter(name=form.cleaned_data.get('name') )):
                return HttpResponse('<h1>This category name is exist</h1>')    
                return redirect('new_category')
            else:
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

def delete_category(request, category_id):
   category = Category.objects.get(pk = category_id)
   category .delete()
   return redirect('show')
