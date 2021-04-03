from django.urls import path
from pusers.views import test, register_view, activate, login_view, logout_view, user_profile,user_profile_update , send_delete_email , delete_account
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url


app_name = 'pusers'

urlpatterns = [
    path('', test, name='home'),
    path('register', register_view, name='register'),
    path('activate/<uidb64>/<time>',activate, name='activate'),
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    # path('projects', list_projects, name='projects'),
    # path('donations', donations_list, name='donations'),
    path('profile',user_profile,name="profile"),
    path('profile/update',user_profile_update,name="profile_update"),
    path('profile/delete/request',send_delete_email,name="delete_request"),
    path('profile/delete/response/<uidb64>/<time>',delete_account, name='account_delete'),


]