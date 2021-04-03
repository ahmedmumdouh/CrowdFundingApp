from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import datetime
from .models import Comments
from .forms import NewCommentForm

# Create your views here.


# @login_required
def new_comment(request):
 
#    user=User.objects.frist()

    all_comment=Comments.objects.all()
    if request.method == 'POST':

        form=NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save
            # comment.save()
            comment=Comments.objects.create(

                comment=form.cleaned_data.get('comment')
                # user_id=user
                #  user_id=1,
                # project_id=1
            )
            return redirect('new_comment')


    else:
        form=NewCommentForm()

 
    
    return render(request,'new_comments.html',{'commentm':all_comment,'form':form})

def show(request):
     all_comment=Comments.objects.all()
     return render(request,'show.html',{'comments':all_comment})
  
def edit(request,comment_id):
      all_comment=get_object_or_404(Comments,pk=comment_id)
      if request.method == 'POST':
            form=NewCommentForm(request.POST)
            if form.is_valid():
                comment = form.save
                all_comment.comment=form.cleaned_data.get('comment')
                all_comment.save()
                return redirect('new_comment')

      else:
        form=NewCommentForm()

      return render(request,'edit_comment.html',{'commentm':all_comment,'form':form})

def delete(request, comment_id):
   comment = Comments.objects.get(pk = comment_id)
   comment .delete()
   return redirect('new_comment')
#    return HttpResponse('deleted')