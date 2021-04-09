from django.shortcuts import render, get_object_or_404, redirect
from projects.models import Project, Picture, Tag, ProjectRate
from django.db.models import Avg
from comments.models import Comments
from reports.forms import ReportProjectForm, ReportCommentForm
from reports.models import ReportProject, ReportComment
from .models import Donate
from pusers.models import PUsers
from home.models import Category
from comments.forms import NewCommentForm
from .forms import NewDonateForm
import datetime
from django.db.models import Q
from django.http import JsonResponse
from django.http import HttpResponse


def index(request):
    projects = Project.objects.select_related('category')
    return render(request, 'projects/index.html', {'projects': projects})


def Create(request):

    if request.method == "GET":
        project = Project(None)
        category = Category.objects.all()
        return render(request, 'projects/add.html', {'new_project': project, 'category': category})
    else:
        project = Project(
            title=request.POST.get('title'),
            details=request.POST.get('details'),
            category_id=request.POST.get('category'),
            total_target=request.POST.get('total_target'),
            start_date=request.POST.get('s_date'),
            end_date=request.POST.get('e_date'),
            owner_id=request.user.id
        )
        if project.clean():
            project.save()
            uploadImages(request, Project.objects.last())
            uploadTags(request.POST.get('tags').split(),
                       Project.objects.last())
            return redirect('projects')
        else:
            category = Category.objects.all()
            return render(request, 'projects/add.html', {'new_project': project, 'category': category})


def uploadImages(images, project):
    for file in images.FILES.getlist('images'):
        file_name = str(file)
        indexofdot = file_name.index('.')
        ext = file_name[indexofdot:len(file_name)]
        file_name = file_name[:indexofdot]
        file.name = file_name + '_' + str(datetime.datetime.now()) + ext
        image = Picture.objects.create(
            project=project,
            image=file
        )


def uploadTags(tags, project):
    for tag_name in tags:
        newTag = Tag.objects.create(
            project=project,
            tag=tag_name
        )


#, commentID


def show(request, project_id, comment_id = 0):
    project = get_object_or_404(Project, id=project_id)
    images = Picture.objects.filter(project_id=project_id)
    tags = Tag.objects.filter(project_id=project_id)
    comments = Comments.objects.filter(project_id=project_id)
    category = Category.objects.get(id=project.category_id)
    current_user = request.user
    userObject = PUsers.objects.get(id=current_user.id)
    tags_array = []
    for tag in tags:
        tags_array.append(tag.tag)
    related_projects = Tag.objects.filter(tag__in=tags_array).exclude(
        project_id__in=[project.id]).select_related('project').values('project').distinct()[:4]
    related_projects_images = []
    for related_project in related_projects:
        related_images = Picture.objects.filter(
            project_id=related_project['project'])[:1]
        related_projects_images += related_images
    all_comment = Comments.objects.all()
    current_user = request.user
    # /////////////////////////////////////////////////////////////////////////////
    rate_of_project =ProjectRate.objects.values('project_id').annotate(average_rating=Avg('value')).filter(project_id = project_id)


   
    #//////////////////////////////////////////////////////////////////////////////////////////////
    current_user = request.user
    if request.method == 'POST':
        formformReportComment = ReportCommentForm(request.POST)
        if formformReportComment.is_valid():
            report = ReportComment.objects.create(
                title=formformReportComment.cleaned_data.get('title'),
                body_comment=formformReportComment.cleaned_data.get('body_comment'),
                comment_id=comment_id,
                user_id=current_user.id
            )
            return redirect('viewProject', project_id=project.id)
    # else:
    #     form = ReportCommentForm()
    #     return render(request, "reports/create_comment.html",
    #                   {'form': form, 'commentId': commentId, 'projectId': project.id})

    if request.method == 'POST':
        formReportProject = ReportProjectForm(request.POST)
        current_user = request.user
        if formReportProject.is_valid():
            # form.save()
            report = ReportProject.objects.create(
                title=formReportProject.cleaned_data.get('title'),
                body_project=formReportProject.cleaned_data.get('body_project'),
                project_id=project.id,
                user_id=current_user.id
            )
            return redirect('viewProject', project_id = project.id)
    # else:
    #     formReport = ReportProjectForm()
    #     return render(request, "projects/view.html", {'formReport': formReport, 'projectId': projectId})
    #     # return render(request, "reports/create_project.html", {'form': form,'projectId':projectId})

    #//////////////////////////////////////////////////////////////////////////////
    if request.method == 'POST':
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save
            comment = Comments.objects.create(
                comment=form.cleaned_data.get('comment'),
                user_id_id=current_user.id,
                project_id_id=project_id
            )

            return redirect('viewProject', project_id=project_id)
    else:
        form = NewCommentForm
    projectObject = Project.objects.get(id=project_id)
    # user=User.objects.frist()
    all_donate = Donate.objects.all()
    current_user = request.user
    # username=PUsers.objects.filter(id=current_user.id)
    if request.method == 'POST':

        formm = NewDonateForm(request.POST)
        if formm.is_valid():
            # donate = form.save
            donate = Donate.objects.create(

                value=formm.cleaned_data.get('value'),
                # user_id=user
                owner_id=current_user.id,
                project_id=project_id
            )

            projectObject.total_donate += formm.cleaned_data.get('value')
            projectObject.save()

            return redirect('viewProject', project_id=project_id)
    else:
        formm = NewDonateForm
    # return render(request,'view.html',{'donates':all_donate,'formm':formm})
    #rate//////////////////////////////////////////////////////////////
    if request.method == 'GET':
        projectObject = Project.objects.get(id=project_id)
    elif request.method == 'POST':
        val = request.POST.get('val')
        obj = ProjectRate.objects.filter(
            project_id=project_id, owner_id=current_user.id).first()
        if (obj):
            obj.value = val
            obj.save()
            return JsonResponse({'success': 'true', 'value': val}, safe=False)
        else:
            rate = ProjectRate.objects.create(

                value=val,
                owner_id=current_user.id,
                project_id=project_id
            )
            return JsonResponse({'success': 'true', 'value': val}, safe=False)
    else:
        return JsonResponse({'success': 'false'})

    # return render(request, 'project_rate.html')   
    #/////////////////////////////////////////////////////////////////
    #Report section

    formReportProject = ReportProjectForm()

    formReportComment = ReportCommentForm()

      #  'commentId': commentId,

    return render(request, 'projects/view.html',
                  {
                      'project': project,
                      'images': images,
                      'tags': tags,
                      'comments': comments,
                      'userObject': userObject,
                      'category': category,
                      'related_projects_images': related_projects_images,
                      'commentm': all_comment,
                      'form': form,
                      'donates': all_donate,
                      'formm': formm,
                      'object': projectObject,
                      'formReportProject': formReportProject,
                      'formReportComment': formReportComment,
                      'rate_of_project': rate_of_project,
                      'current_user':current_user

                  })


def update(request, project_id):
    if request.method == "GET":
        project = get_object_or_404(Project, id=project_id)
        tags = Tag.objects.filter(project_id=project_id)
        tagValues = ''
        for tag in tags:
            tagValues += tag.tag + ' '
        category = Category.objects.all()
        return render(request, 'projects/edit.html', {'project_dict':  project, 'category': category, 'tags': tagValues})
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
        if tagValues == request.POST.get('tags'):
            # if upload new images
            if request.FILES:
                # update images only here
                deleteOldImages(project)
                uploadImages(request, project)
        else:
            # if images and tags changed
            if request.FILES:
                # update image and tags here
                deleteOldImages(project)
                uploadImages(request, project)
                deleteOldTags(tags)
                uploadTags(request.POST.get('tags').split(), project)
            else:
                # if tags only changed
                deleteOldTags(tags)
                uploadTags(request.POST.get('tags').split(), project)
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
    project = get_object_or_404(Project, id=project_id)
    if project.total_donate <  (project.total_target * 25/100 ):
        deleteOldImages(project)
        project.delete()
        return redirect('/projects/my_projects?status=project deleted successfully')
    else:
        return  redirect('/projects/my_projects?status=you can\'t delete this project')


def rate_project(request, projectId):
    current_user = request.user
    if request.method == 'GET':

        projectObject = Project.objects.get(id=projectId)
        context = {

            'object': projectObject}
        return render(request, 'project_rate.html', context)

    elif request.method == 'POST':
        val = request.POST.get('val')
        obj = ProjectRate.objects.filter(
            project_id=projectId, owner_id=current_user.id).first()
        if (obj):
            obj.value = val
            obj.save()
            return JsonResponse({'success': 'true', 'value': val}, safe=False)
        else:
            rate = ProjectRate.objects.create(

                value=val,
                owner_id=current_user.id,
                project_id=projectId
            )
            return JsonResponse({'success': 'true', 'value': val}, safe=False)
    else:
        return JsonResponse({'success': 'false'})

    return render(request, 'project_rate.html')


def list_my_projects(request):
    my_projects = Project.objects.filter(owner_id=request.user.id)
    status = request.GET.get('status')
    return render(request,'projects/my_projects.html',{'projects':my_projects,'status':status})
