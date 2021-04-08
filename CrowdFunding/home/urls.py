
from django.urls import path , include
from . import views


urlpatterns = [
    path('',  views.index, name='index'),
    path('new_category',  views.new_category , name='new_category'),
    path('show',  views.show, name='show'),
    path('searchName', views.searchName, name='searchName'),
    path('searchTag', views.searchTag, name='searchTag'),
    path('delete/<int:category_id>',  views.delete_category , name='delete_category'),

]


