from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
import datetime
from .models import Comments
from .forms import NewCommentForm
from  pusers.models import PUsers

# Create your views here.


# @login_required
def new_comment(request,projectId):
 
#    user=User.objects.frist()


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
                 user_id_id=current_user.id,
                 project_id_id=projectId
            )
            
            return redirect('viewProject',project_id=projectId)
    else:
        form=NewCommentForm
    return render(request,'new_comments.html',{'commentm':all_comment,'form':form})


def edit(request,comment_id,projectId):
      all_comment=get_object_or_404(Comments,pk=comment_id)
      if request.method == 'POST':
            form=NewCommentForm(request.POST)
            if form.is_valid():
                comment = form.save
                all_comment.comment=form.cleaned_data.get('comment')
                all_comment.save()
                return redirect('viewProject',project_id=projectId)

      else:
        form=NewCommentForm()

      return render(request,'edit_comment.html',{'commentm':all_comment,'form':form})

def delete(request, comment_id,projectId):
   comment = Comments.objects.get(pk = comment_id)
   comment .delete()
   return redirect('viewProject',project_id=projectId)
#    return HttpResponse('deleted')