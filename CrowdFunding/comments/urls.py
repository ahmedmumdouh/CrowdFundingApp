
from django.urls import path , include
from . import views


urlpatterns = [
    path('new_comments/<int:projectId>',  views.new_comment , name='new_comment'),
    # path('/show_comment',  views.show_comment , name='show_comment'),
    # path('show',  views.show , name='show'),
    path('edit/<int:projectId>/<int:comment_id>',  views.edit , name='edit_comment'),
    path('delete/<int:projectId>/<int:comment_id>',  views.delete , name='delete_comment'),
    
    
    

]
# localhost:223/projects/view/1/new_comment


