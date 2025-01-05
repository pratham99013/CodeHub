
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.projects, name = "projects"),
    path('create-project/', views.createProject, name="createproject"),
    path('view-project/<str:pk>/', views.viewproject, name="viewproject"),
    path('update-project/<str:pk>/' , views.updateProject, name = "updateproject"),
    path('delete-project/<str:pk>/' , views.deleteproject, name = "deleteproject")
]
