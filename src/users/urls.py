from knox import views as knox_views
from users.api import LoginAPI, GetLoggedUserAPI
from django.urls import path

urlpatterns = [
     path('login', LoginAPI.as_view(), name='login'),
     path('user', GetLoggedUserAPI.as_view(), name='user'),
     path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]