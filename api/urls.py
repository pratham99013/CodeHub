from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('' , views.getroutes, name = "api"),
    path('projects/' , views.getprojects, name = "okau"),
    path('projects/<str:pk>/' , views.getproject, name = "okay"),
      path('projects/<str:pk>/views/' , views.projectVote, name = "oy"),
 
] 
