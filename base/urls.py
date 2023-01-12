from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # AUTH
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # USER
    path('update-user/', views.updateUser, name='update-user'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),

    # FORUM
    path('forum/', views.homeForum, name='forum-home'),
    path('forum/room/<str:pk>/', views.room, name='room'),
    path('forum/create-room', views.createRoom, name='create-room'),
    path('forum/update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('forum/delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('forum/delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),

] 

