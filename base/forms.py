from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Room, Book, LibraryBook, ReadingGroup, Session
from django import forms


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class TimeInput(forms.TimeInput):
    input_type = "time"


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)
        
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
        
class ReadingGroupForm(ModelForm):
    class Meta:
        model = ReadingGroup
        fields = '__all__'
        exclude = ['library', 'users']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_finale"].widget = DateInput()
        
class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = [ 'date_seance']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date_seance"].widget = DateInput()
       