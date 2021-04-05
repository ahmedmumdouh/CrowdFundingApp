
from django.urls import path
from . import views


urlpatterns = [
     path('create-for-comment/<int:projectId>/<int:commentId>', views.create_report_comment, name='create_report_comment'),
     path('create-for-project/<int:projectId>', views.create_report_project, name='create_report_project'),
     path('show-for-project/', views.show_report_project, name='show_report_project'),
     path('show-for-comment/', views.show_report_comment, name='show_report_comment'),
     path('delete-for-comment/<id>', views.delete_report_comment, name='delete_report_comment'),
     path('delete-for-project/<id>', views.delete_report_project, name='delete_report_project'),

]


