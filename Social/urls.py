from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signout', views.logout_user, name='sign out'),
    path('signin', views.login_user, name='sign in'),
    path('signup', views.signup, name='sign up'),
    path('search', views.search, name='search'),
    path('search-user', views.search_user, name='search_user'),
    path('profile list', views.profileList, name='profile list'),
    path('update profile', views.updateProfile, name='update profile'),
    path('twit-like/<int:pk>', views.twit_like, name='twit_like'),
    path('twit-share/<int:pk>', views.twit_share, name='twit_share'),
    path('twit-delete/<int:pk>', views.twit_delete, name='twit_delete'),
    path('twit-edit/<int:pk>', views.twit_edit, name='twit_edit'),
    path('unfollow/<int:pk>', views.unfollow, name='unfollow'),
    path('follow/<int:pk>', views.follow, name='follow'),
    path('<str:username>-followers', views.followers, name='followers'),
    path('<str:username>-following', views.following, name='following'),
    path('<str:username>', views.profile, name='profile'),
]