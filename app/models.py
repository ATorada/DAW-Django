from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class ProfileEvent(models.Model):
    profile = models.CharField(max_length=100)
    event = models.CharField(max_length=100)

    def __str__(self):
        return self.profile + ' - ' + self.event

""" class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='member')
    birthday = models.DateField(null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    twitch = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name """
        
#Crea el modelo de usuario junto al modelo de usuario de django
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    id_user = models.IntegerField()
    role = models.CharField(max_length=100, default='member')
    birthday = models.DateField(null=True, blank=True)
    twitter = models.CharField(max_length=100, null=True, blank=True)
    twitch = models.CharField(max_length=100, null=True, blank=True)
    instagram = models.CharField(max_length=100, null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    text = models.TextField()
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    visibility = models.BooleanField(default=False)
    date = models.DateField(null=True, blank=True)
    hour = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name