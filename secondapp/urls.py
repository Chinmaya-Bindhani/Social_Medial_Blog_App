from django.urls import path
from .views import log_out,register,profile
from django.contrib.auth import views as auth_views


urlpatterns=[
 path('logout/',log_out,name='logout'),
 path('login/',auth_views.LoginView.as_view(
     template_name='blog/login.html'
 ),name='login'),
 path(
     'register/',register,name='register'
 ),
path('profile/',profile,name='profile')

]