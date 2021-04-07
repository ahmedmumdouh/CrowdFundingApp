
from django.urls import path , include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',  views.index , name='projects'),
    path('create', views.Create, name='newProject'),
    path('view/<int:project_id>',views.show, name='viewProject'),
    path('edit/<int:project_id>',views.update, name='editProject'),
    path('new_rate/<int:projectId>',views.new_rate, name='new_rate'),
    path('project_rate/<int:projectId>',views.rate_project, name='project_rate'),
    path('new_donate.html/<int:projectId>',views.new_donate, name='new_donate'),
    path('delete/<int:project_id>',views.deleteProject, name='deleteProject'),

    
   
    
]


