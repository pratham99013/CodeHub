from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutUser, name = 'logout'),
    path('register/', views.RegisterUser, name = 'register'),
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userprofile, name='user-profile'),
    path('account/' , views.userAccount, name= 'account'),
    path('editaccount/' , views.editAccount, name= 'editaccount'),
    path('createskill/' , views.createSkill, name= 'createskill'),
    path('deleteskill/<str:pk>/' , views.deleteSkill, name= 'deleteskill'),
    path('inbox/' , views.inbox, name= 'inbox'),
    path('message/<str:pk>/' , views.viewmessage, name= 'message'),
    path('sendmessage/<str:pk>/' , views.createmessage, name= 'createmessage'),
]
