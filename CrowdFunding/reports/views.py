from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseForbidden
from .models import *
from .forms import ReportCommentForm, ReportProjectForm
from .models import ReportProject, ReportComment



def create_report_project(request):
    if request.method == 'POST':
        form = ReportProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show_report_project')
    else:
        form = ReportProjectForm()
        return render(request, "reports/create_project.html", {'form': form})


def create_report_comment(request):
    if request.method == 'POST':
        form = ReportCommentForm(request.POST)
        if form.is_valid():

            form.save()
            return redirect('show_report_comment')
    else:
        form = ReportCommentForm()
        return render(request, "reports/create_comment.html", {'form': form})


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







