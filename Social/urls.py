from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signout', views.logout_user, name='sign out'),
    path('signin', views.login_user, name='sign in'),
    path('signup', views.signup, name='sign up'),
    path('profile list', views.profileList, name='profile list'),
    path('update profile', views.updateProfile, name='update profile'),
    path('<str:username>', views.profile, name='profile'),
]