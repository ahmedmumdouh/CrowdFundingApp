from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from .models import *
from .forms import ReportCommentForm, ReportProjectForm
from .models import ReportProject, ReportComment


def create_report_project(request, projectId):
    if request.method == 'POST':
        form = ReportProjectForm(request.POST)
        current_user = request.user
        if form.is_valid():
            # form.save()
            report = ReportProject.objects.create(
                title=form.cleaned_data.get('title'),
                body_project=form.cleaned_data.get('body_project'),
                project_id=projectId,
                user_id=current_user.id
            )
            return redirect('viewProject', {"project_id": projectId})
    else:
        form = ReportProjectForm()
        return render(request, "projects/view.html", {'formreportproject': form,'projectId': projectId})
        # return render(request, "reports/create_project.html", {'form': form,'projectId':projectId})


def create_report_comment(request, projectId, commentId):
    current_user = request.user
    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():
            report=ReportComment.objects.create(
                title=form.cleaned_data.get('title'),
                body_comment=form.cleaned_data.get('body_comment'),
                comment_id=commentId,
                user_id=current_user.id
            )
            return redirect('viewProject', project_id=projectId)
    else:
        form = ReportCommentForm()
        return render(request, "reports/create_comment.html", {'form': form, 'commentId': commentId, 'projectId': projectId})


def show_report_comment(request):
    all_comments = ReportComment.objects.all()
    context = {
            "all_comments": all_comments
       }
    return render(request, 'reports/showRC.html', context)


def show_report_project(request):
    all_projects = ReportProject.objects.all()
    context = {
        "all_projects": all_projects
    }
    return render(request, 'reports/showRP.html', context)


def delete_report_project(request,id):
    ReportProject.objects.filter(id=id).delete()
    return redirect('show_report_project')


def delete_report_comment(request,id):
    ReportComment.objects.filter(id=id).delete()
    return redirect('show_report_comment')







