from knox import views as knox_views
from users.api import LoginAPI, GetLoggedUserAPI, SignUpUserAPI
from django.urls import path

urlpatterns = [
     path('login', LoginAPI.as_view(), name='login'),
     path('user', GetLoggedUserAPI.as_view(), name='user'),
     path('user/new', SignUpUserAPI.as_view(), name='sign_up'),
     path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
     path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),
]