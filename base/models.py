from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

# USER
class User(AbstractUser):
  USER = 1
  SELLER = 2
      
  ROLE_CHOICES = (
      (USER, 'User'),
      (SELLER, 'Seller'),
  )
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)


# FORUM
class Topic(models.Model):
  name = models.CharField(max_length=100)

  def __str__(self):
    return self.name

class Room(models.Model):
  host          = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  topic         = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
  name          = models.CharField(max_length=100)
  description   = models.TextField(null=True, blank=True)
  participants  = models.ManyToManyField(User, related_name='participants', blank=True)
  updated       = models.DateTimeField(auto_now=True)
  created       = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.name
    

class Message(models.Model):
  user    = models.ForeignKey(User, on_delete=models.CASCADE)
  room    = models.ForeignKey(Room, on_delete=models.CASCADE)
  body    = models.TextField()
  updated = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)

  class Meta:
    ordering = ['-updated', '-created']

  def __str__(self):
    return self.body[0:50]
  
  
# BOOK

class Collection(models.Model):
  name = models.CharField(max_length=100)
  
class Genre(models.Model):
  name = models.CharField(max_length=100)
  
class Book(models.Model):
  title = models.CharField(max_length=100)
  author = models.CharField(max_length=100)
  cover = models.ImageField(upload_to='covers/', default='default.jpeg', null=True, blank=True)
  publisher = models.CharField(max_length=100)
  collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, null=True)
  genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
  libraries = models.ManyToManyField('Library', through='LibraryBook', related_name='library')



# LIBRARY

class Localization(models.Model):
  adresse = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  zipCode = models.IntegerField
  country = models.CharField(max_length=100)


class Library(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  books = models.ManyToManyField(Book, through='LibraryBook')
  name = models.CharField(max_length=100)
  localization = models.ForeignKey(Localization, on_delete=models.SET_NULL, null=True)
  created = models.DateTimeField(auto_now_add=True)
  def __str__(self):
        return self.name

  
class LibraryBook(models.Model):
  library = models.ForeignKey(Library, on_delete=models.CASCADE)
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  borrowingUser = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
  borrowed = models.BooleanField(default=False)
  date = models.DateTimeField(null=True)
  
  def save(self, *args, **kwargs):
        if self.date is None:
            self.date = datetime.now() + datetime.timedelta(days=30)
        super(LibraryBook, self).save(*args, **kwargs)
  class Meta:
    ordering = ['-date']
  def __str__(self):
        return "{}_{}".format(self.library.__str__(), self.book.__str__())

  

  
