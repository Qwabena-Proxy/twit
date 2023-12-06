from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('SignOut', views.logout, name='sign out'),
    path('profile list', views.profileList, name='profile list'),
    path('<str:username>', views.profile, name='profile'),
]