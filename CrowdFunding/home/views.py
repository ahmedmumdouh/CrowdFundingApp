from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import datetime
from .models import Category
from .forms import NewCategoryForm


# Create your views here.

def index(request):
   return  render(request , 'home/index.html')

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
     all_category=Category.objects.all()
     return render(request,'category/show.html',{'category':all_category})
