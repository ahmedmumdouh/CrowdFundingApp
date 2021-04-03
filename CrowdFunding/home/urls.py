
from django.urls import path , include
from . import views


urlpatterns = [
    path('',  views.index , name='index'),
    path('new_category',  views.new_category , name='new_category'),
]


