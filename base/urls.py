from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),

    # AUTH
    path('login/', views.loginPage, name='login'),
    path('register/', views.registerPage, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    # USER
    path('update-user/', views.updateUser, name='update-user'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('home/', views.user_home, name='user-home'),

    # FORUM
    path('forum/', views.homeForum, name='forum-home'),
    path('forum/room/<str:pk>/', views.room, name='room'),
    path('forum/create-room', views.createRoom, name='create-room'),
    path('forum/update-room/<str:pk>/', views.updateRoom, name='update-room'),
    path('forum/delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('forum/delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
    
    # BOOK
    path('books/', views.books, name='books-home'),
    path('books/create-book', views.create_book, name='create-book'),
    path('books/update-book/<str:pk>/', views.update_book, name='update-book'),
    path('books/borrowed-books/', views.borrow_books, name='borrow-by-user'),
    path('books/library/<str:pk>/', views.add_to_library, name='add-to-library'),
    path('books/borrow/<str:pk>/', views.borrow_book, name='borrow-book'),
    path('books/return-book/<str:pk>/', views.return_book, name='return-book'),

    

    # READING GROUP
    path('reading_group/', views.home_reading_group, name='reading-group-home'),
    path('reading_group/create-reading-group/', views.create_reading_group, name='create-reading-group'),
    path('reading_group/update-reading-group/<str:pk>/', views.update_reading_group, name='update-reading-group'),
    path('reading_group/delete-reading-group/<str:pk>/', views.delete_reading_group, name='delete-reading-group'),
    path('reading_group/<str:pk>/participate', views.participe_reading_group, name='particate-reading'),
    path('reading_group/<str:pk>/leave', views.leave_reading_group, name='leave-reading'),
    path('reading_group/<str:pk>/session', views.create_session, name='create-session'),
    
]   



if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

