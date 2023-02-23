from django.contrib import admin

# Register your models here.
from .models import Profile, Event, ProfileEvent, Message

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(ProfileEvent)
admin.site.register(Message)
