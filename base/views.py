from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.db.models import Case, When, Value
from applib.decorators import seller_required
from datetime import datetime, timedelta

from .models import User, Room, Topic, Message, Book, Collection, Genre, LibraryBook
from .forms import RoomForm, MyUserCreationForm, BookForm

def home(request):
    return render(request, 'base/home.html')

# ============== AUTH ======================
def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f"Username or Password does not exist")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, f'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})


# ============== USER ======================
def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = MyUserCreationForm(instance=user)
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update_user.html', {'form': form})


# ============== ROOM ======================
def homeForum(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    )
    topics = Topic.objects.all()
    # room_count = Room.objects.all().count()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q)
    )

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'forum/home_forum.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'forum/room.html', context)


@login_required(login_url='login')
def createRoom(request): 
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('forum-home')
    context = {'form': form, 'topics': topics}
    
    return render(request, 'forum/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('forum-home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'forum/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here')

    if request.method == 'POST':
        room.delete()
        return redirect('forum-home')

    return render(request, 'forum/delete_room.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to delete this message')

    if request.method == 'POST':
        message.delete()
        return redirect('forum-home')

    return render(request, 'forum/delete_room.html', {'obj': message})    


# ============== BOOK ======================
@login_required(login_url='login')
def books(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    books = Book.objects.filter(
        Q(collection__name__icontains=q) | 
        Q(genre__name__icontains=q) | 
        Q(title__icontains=q) | 
        Q(publisher__icontains=q) | 
        Q(author__icontains=q) |
        Q(libraries__name__icontains=q)
    )
    user_id = request.user.id
    library_books = LibraryBook.objects.filter(
         Q(book__collection__name__icontains=q) | 
        Q(book__genre__name__icontains=q) | 
        Q(book__title__icontains=q) | 
        Q(book__publisher__icontains=q) | 
        Q(book__author__icontains=q) |
        Q(library__name__icontains=q)
    ).exclude(borrowingUser__id=user_id)
        
    context = {'books': books, 'library_books': library_books}
    return render(request, 'book/book.html', context) 

@login_required(login_url='login')
@seller_required
def create_book(request):
    form = BookForm()
    collections = Collection.objects.all()
    genres = Genre.objects.all()
    if request.method == 'POST':
        collection_name = request.POST.get('collection')
        collection, create = Collection.objects.get_or_create(name=collection_name)
        
        genre_name = request.POST.get('genre')
        genre, create = Genre.objects.get_or_create(name=genre_name)

        cover = 'covers/default.jpeg'
        if request.FILES:
            cover = request.FILES['cover']
        book = Book.objects.create(
            genre=genre,
            collection=collection,
            title=request.POST.get('title'),
            author=request.POST.get('author'),
            publisher=request.POST.get('publisher'),
            cover=cover,
        )
        
            
        return redirect('books-home')

    context = {'form': form, 'collections': collections, 'genres': genres}
    return render(request, 'book/book_form.html', context)

@login_required(login_url='login')
@seller_required
def update_book(request, pk):
    book = Book.objects.get(id=pk)
    form = BookForm(instance=book)
    collections = Collection.objects.all()
    genres = Genre.objects.all()
    if request.method == 'POST':
        collection_name = request.POST.get('collection')
        collection, create = Collection.objects.get_or_create(name=collection_name)
        
        genre_name = request.POST.get('genre')
        genre, create = Genre.objects.get_or_create(name=genre_name)

        cover = 'covers/default.jpeg'
        if request.FILES:
            cover = request.FILES['cover']
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publisher = request.POST.get('publisher')
        book.cover = cover
        book.collection = collection
        book.genre = genre
        book.save()
        return redirect('books-home')

    context = {'form': form, 'collections': collections, 'genres': genres, 'book': book}
    return render(request, 'book/book_form.html', context)

# ============== USER HOME ======================
@login_required(login_url='login')
def user_home(request):
    library_books = LibraryBook.objects.filter(borrowingUser=request.user, borrowed=True)
    context = {'libraryBooks': library_books}
    return render(request, 'user/user_home.html', context)

@login_required(login_url='login')
def borrow_book(request, pk_book, pk_library):
    library_book, create = LibraryBook.objects.get_or_create(book_id=pk_book, library_id=pk_library)
    library_book.borrowingUser = request.user
    library_book.borrowed = True
    library_book.date = datetime.now() + timedelta(days=30)
    library_book.save()
    return redirect('user-home')

@seller_required
def borrow_books(request):
   
    return render(request, 'book/borrowed-books.html')
