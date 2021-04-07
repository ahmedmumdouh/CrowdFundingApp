from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import datetime
from .models import Category

from .forms import NewCategoryForm
from projects.models import Project
from projects.models import Picture
from projects.models import Tag




# Create your views here.

def index(request):
    all_category= Category.objects.all()
    latest_projects = Project.objects.order_by('start_date')[:5]
    images = [] 
    for project in latest_projects:
        images.append(Picture.objects.filter(project_id=project.id).first())

    context = {
        'all_category': all_category,
        'latest_projects': latest_projects,
        'images' : images
    }
    return  render(request , 'home/index.html',context )

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
