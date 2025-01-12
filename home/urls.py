from django.contrib import admin
from django.urls import path , include
from home import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login', views.loginUser, name="login"),
    path('logout', views.logoutUser, name="logout"),
    path('allposts', views.allposts, name="allposts"),
    path('add_post', views.add_post, name="add_post"),
    path('edit_post/<str:post_id>/', views.edit_post, name="edit_post"),
    path('delete_post/<str:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name="search"),
    path('base/', views.base, name="base"),

]
