
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('where', views.where, name='where'),
    path('cookie-settings', views.cookie_settings, name='cookie-settings'),
    path('cookie-policy', views.cookie_policy, name='cookie-policy'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('terms', views.terms, name='terms'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('events/<int:event>/join', views.joinEvent, name='events.join'),
    path('events/<int:event>/leave', views.leaveEvent, name='events.leave'),
    path('events', views.indexEvent, name='events.index'),
    path('events/create', views.createEvent, name='events.create'),
    path('events/<int:event>', views.showEvent, name='events.show'),
    path('events/<int:event>/edit', views.editEvent, name='events.edit'),
    path('events/<int:event>/destroy', views.destroyEvent, name='events.destroy'),
    path('messages/create', views.createMessages, name='messages.create'),
    path('messages', views.indexMessages, name='messages.index'),
    path('messages/<int:message>/destroy', views.destroyMessages, name='messages.destroy'),
    path('messages/<int:message>', views.showMessages, name='messages.show'),
    path('users', views.indexUsers, name='users.index'),
    path('users/<int:user>', views.showUsers, name='users.show'),
    path('users/<int:user>/edit', views.editUsers, name='users.edit'),
]