
from django.urls import path , include
from . import views


urlpatterns = [
    path('new_comments',  views.new_comment , name='new_comment'),
    # path('/show_comment',  views.show_comment , name='show_comment'),
     path('show',  views.show , name='show'),
      path('edit/<int:comment_id>',  views.edit , name='edit_comment'),
    
    
    

]


