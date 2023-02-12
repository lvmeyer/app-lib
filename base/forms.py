from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Room, Book, LibraryBook

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']


# class UserForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        
class LibraryBookForm(ModelForm):
    class Meta:
        model = LibraryBook
        fields = '__all__'
        exclude = [ 'book', 'library', 'borrowed', 'date']