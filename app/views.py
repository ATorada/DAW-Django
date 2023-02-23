from django.shortcuts import render, redirect
from django.http import HttpResponse
from app.models import Profile, ProfileEvent, Event, Message
from django.contrib.auth.models import User, auth
import json

# Create your views here.

""" 
    path('events/<int:event>/join', views.joinEvent, name='events.join'),
    path('events/<int:event>/leave', views.leaveEvent, name='events.leave'),
    path('events', views.indexEvent, name='events.index'),
    path('events/create', views.createEvent, name='events.create'),
    #path('events/store', views.store, name='events.store'),
    path('events/<int:event>', views.showEvent, name='events.show'),
    path('events/<int:event>/edit', views.editEvent, name='events.edit'),
    #path('events/<int:event>/update', views.update, name='events.update'),
    path('events/<int:event>/destroy', views.destroyEvent, name='events.destroy'),
    path('messages/create', views.createMessages, name='messages.create'),
    #path('messages/store', views.store, name='messages.store'),
    path('messages', views.indexMessages, name='messages.index'),
    path('messages/<int:message>/destroy', views.destroyMessages, name='messages.destroy'),
    path('messages/<int:message>', views.showMessages, name='messages.show'),
    path('users', views.indexUsers, name='users.index'),
    path('users/<int:user>', views.showUsers, name='users.show'),
    path('users/<int:user>/edit', views.editUsers, name='users.edit'),
    #path('users/<int:user>/update', views.update, name='users.update'),
    path('users/<int:user>/destroy', views.destroyUsers, name='users.destroy'),, """

""" def home(request):
    return HttpResponse('Django funciona') """
    
def index(request):
    if request.user.is_authenticated:
        #Se obtiene el perfil del usuario
        profile = Profile.objects.get(user=request.user)
        return render(request, 'index.html', {'isAdmin': profile.role == 'admin'})
    else:
        return render(request, 'index.html')

def where(request):
    if request.user.is_authenticated:
        #Se obtiene el perfil del usuario
        profile = Profile.objects.get(user=request.user)
        return render(request, 'where.html', {'isAdmin': profile.role == 'admin'})
    else:
        return render(request, 'where.html')

def cookie_settings(request):
    return render(request, 'static/cookie_settings.html')

def cookie_policy(request):
    return render(request, 'static/cookie_policy.html')

def privacy_policy(request):
    return render(request, 'static/privacy_policy.html')

def terms(request):
    return render(request, 'static/terms.html')

def register(request):
    if request.method == 'POST':
        #Obtiene los datos del formulario
        if request.POST['name'] == '':
            return render(request, 'auth/register.html', {'error': 'El campo nombre es obligatorio'})
        if request.POST['email'] == '':
            return render(request, 'auth/register.html', {'error': 'El campo correo es obligatorio'})
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password_confirmation']
        #Verifica que las contraseñas coincidan
        if password == password2 and password != '':
            #Verifica que el usuario no exista
            if User.objects.filter(email=email).exists():
                return render(request, 'auth/register.html', {'error': 'Ya se ha registrado un usuario con este correo'})
            else:
                #Crea un objeto usuario
                username = email.split('@')[0]
                user = User.objects.create_user(username=username ,email=email, password=password)
                user.save()
                auth.login(request, user)
                
                new_profile = Profile.objects.create(user=user, id_user=user.id, name=name, email=email, password=password)
                new_profile.save()
                     
                #Redirecciona a la pagina de inicio
                return redirect('index')
        else:
            return render(request, 'auth/register.html', {'error': 'Las contraseñas no coinciden o están vacías'})
    else:
        return render(request, 'auth/register.html')

def login(request):
    if request.method == 'POST':
        #Obtiene los datos del formulario
        email = request.POST['email']
        password = request.POST['password']
        #Autentica al usuario
        username = email.split('@')[0]
        user = auth.authenticate(username=username, password=password)
        #Si el usuario existe y esta activo
        if user is not None:
            #Inicia la sesion del usuario
            auth.login(request, user)
            #Redirecciona a la pagina de inicio
            return redirect('index')
        else:
            #Devuelve un error al login
            return render(request, 'auth/login.html', {'error': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'auth/login.html')

def logout(request):
    #Cierra la sesion del usuario actual
    auth.logout(request)
    #Redirecciona a la pagina de inicio
    return redirect('index')

def joinEvent(request, event):
    #Une al usuario actual al evento
    if request.user.is_authenticated:
        perfil = Profile.objects.get(user=request.user)
        event = Event.objects.get(id=event)
        new_profile_event = ProfileEvent.objects.create(event=event.id, profile=perfil.id_user)
        new_profile_event.save()
        request.session['success'] = 'Usuario añadido correctamente'
    return redirect('events.show', event.id)

def leaveEvent(request, event):
    #Saca al usuario actual del evento
    if request.user.is_authenticated:
        perfil = Profile.objects.get(user=request.user)
        event = Event.objects.get(id=event)
        ProfileEvent.objects.filter(event=event.id).filter(profile=perfil.id_user).delete()
        request.session['success'] = 'Usuario eliminado correctamente'
    return redirect('events.show', event.id)

def indexEvent(request):
    #Obtiene los eventos de la base de datos
    events = Event.objects.all()
    if request.user.is_authenticated:
        #Se obtiene el perfil del usuario
        profile = Profile.objects.get(user=request.user)
        return render(request, 'events/index.html', {'events': events, 'isAdmin': profile.role == 'admin'})
    else:
        #Envia los eventos a la vista
        return render(request, 'events/index.html', {'events': events})
    

def createEvent(request):
    #Obtiene el usuario y su perfil y comprueba que el perfil sea admin
    if request.user.is_authenticated:
        perfil = Profile.objects.get(user=request.user)
        if perfil.role == 'admin':
            if request.method == 'POST':
                
                messages = []
                #Obtiene los datos del formulario
                if request.POST['name'] == '':
                    messages.append('El campo nombre es obligatorio')
                if request.POST['description'] == '':
                    messages.append('El campo descripción es obligatorio')
                    
                #Se comprueba que la fecha sea una fecha valida
                if request.POST['date']:
                    date = request.POST['date']
                else:
                    date = None
                
                if request.POST['hour']:
                    hour = request.POST['hour']
                else:
                    hour = None
                
                if len(messages) > 0:
                    return render(request, 'events/create.html', {'messages': messages, 'form': request.POST})
                
                #Obtiene los datos del formulario
                name = request.POST['name']
                description = request.POST['description']
                location = request.POST['location']
                visibility = request.POST['visibility']
                tags = request.POST['tags']
                
                #Crea un objeto evento
                new_event = Event.objects.create(name=name, description=description, date=date, hour=hour, visibility=visibility, tags=tags, location=location)
                new_event.save()
                #Redirecciona a la pagina de inicio
                return redirect('events.show', new_event.id)
            else:
                #Obtiene el perfil del usuario actual
                profile = Profile.objects.get(user=request.user)
                return render(request, 'events/create.html', {'isAdmin': profile.role == 'admin'})
        else:
            return redirect('events.index')
    else:
        return redirect('events.index')

def showEvent(request, event):
    #Obtiene el evento de la base de datos
    event = Event.objects.get(id=event)
    #Comprueba si el usuario actual esta en el evento mirando la tabla intermedia de usuarios y eventos
    if request.user.is_authenticated:
        perfil = Profile.objects.get(user=request.user)
        if ProfileEvent.objects.filter(event=event.id).filter(profile=perfil.id_user).exists():
            is_joined = True
        else:
            is_joined = False
    
    if request.session.get('success') is not None:
        success = request.session['success']
        del request.session['success']
    else:
        success = None
    #Obtiene los usuarios del evento
    users = ProfileEvent.objects.filter(event=event.id)
    #Al obtener solo los ids de los usuarios, se hace una consulta a la tabla de usuarios para obtener los datos de los usuarios
    #Lo hace con un bucle for
    usersFinal = []
    for user in users:
        user = Profile.objects.get(id_user=user.profile)
        usersFinal.append(user)

    if request.session.get('success') is not None:
        success = request.session['success']
        del request.session['success']
    
    #Obtiene el perfil del usuario actual
    profile = Profile.objects.get(user=request.user)
    #Envia el evento a la vista
    return render(request, 'events/show.html', {'event': event, 'is_joined': is_joined, 'users': usersFinal, 'success': success, 'isAdmin': profile.role == 'admin', 'success': success})

def editEvent(request, event):
    
    #Obtiene el evento de la base de datos
    event = Event.objects.get(id=event)
    
    if request.method == 'POST':
        messages = []
        #Obtiene los datos del formulario
        if request.POST['name'] == '':
            messages.append('El campo nombre es obligatorio')
        if request.POST['description'] == '':
            messages.append('El campo descripción es obligatorio')
        #Se comprueba que la fecha sea una fecha valida
        if request.POST['date']:
            date = request.POST['date']
        else:
            date = None
        
        if request.POST['hour']:
            hour = request.POST['hour']
        else:
            hour = None
        
        if len(messages) > 0:
            return render(request, 'events/edit.html', {'messages': messages, 'event': event})
        
        name = request.POST['name']
        description = request.POST['description']
        location = request.POST['location']
        tags = request.POST['tags']
        #Obtiene el evento de la base de datos
        event = Event.objects.get(id=event.id)
        #Actualiza los datos del evento
        event.name = name
        event.description = description
        event.date = date
        event.hour = hour
        event.location = location
        event.tags = tags
        event.save()
        
        request.session['success'] = 'Evento actualizado correctamente'
        return redirect('events.show', event.id)
    
    #Obtiene el perfil del usuario logueado
    profile = Profile.objects.get(user=request.user)
    
    return render(request, 'events/edit.html', {'event': event, 'isAdmin': profile.role == 'admin'})
    

def destroyEvent(request, event):
    #Obtiene el evento de la base de datos
    event = Event.objects.get(id=event)
    #Elimina el evento
    event.delete()
    #Elimina los registros de la tabla intermedia de usuarios y eventos
    ProfileEvent.objects.filter(event=event.id).delete()
    #Redirecciona a la pagina de inicio de eventos
    request.session['success'] = 'Evento eliminado correctamente'
    return redirect('events.index')

def createMessages(request):
    
    if request.method == 'POST':
        messages = []
        if request.POST['message'] == '':
            messages.append('El campo mensaje es obligatorio')
        if request.POST['subject'] == '':
            messages.append('El campo asunto es obligatorio')
        if request.POST['email'] == '':
            messages.append('El campo email es obligatorio')
        if request.POST['name'] == '':
            messages.append('El campo nombre es obligatorio')
            
        if len(messages) > 0:
            return render(request, 'messages/create.html', {'messages': messages, 'form': request.POST})
        
        message = request.POST['message']
        new_message = Message.objects.create(text=message, subject=request.POST['subject'], email=request.POST['email'], name=request.POST['name'])
        new_message.save()
        
        request.session['success'] = 'Mensaje enviado correctamente'
        return redirect('messages.create')
    
    if request.session.get('success') is not None:
        success = request.session['success']
        del request.session['success']
    else:
        success = None
    
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        return render(request, 'messages/create.html', {'isAdmin': profile.role == 'admin', 'success': success})
    else:
        return render(request, 'messages/create.html', {'success': success})
    

def indexMessages(request):
    profile = Profile.objects.get(user=request.user)
    #Obtiene los mensajes de la base de datos
    messages = Message.objects.all()
    if request.session.get('success') is not None:
        success = request.session['success']
        del request.session['success']
    else:
        success = None
    return render(request, 'messages/index.html', {'isAdmin': profile.role == 'admin', 'success': success, 'messages': messages})

def destroyMessages(request, message):
    #Obtiene el mensaje de la base de datos
    message = Message.objects.get(id=message)
    #Elimina el mensaje
    message.delete()
    request.session['success'] = 'Mensaje eliminado correctamente'
    return redirect('messages.index')

def showMessages(request, message):
    profile = Profile.objects.get(user=request.user)
    #Obtiene el mensaje de la base de datos
    message = Message.objects.get(id=message)
    message.readed = True
    message.save()
    return render(request, 'messages/show.html', {'isAdmin': profile.role == 'admin', 'message': message})

def indexUsers(request):
    #Obtiene los usuarios de la base de datos
    users = Profile.objects.all()
    if request.user.is_authenticated:
        #Se obtiene el perfil del usuario
        profile = Profile.objects.get(user=request.user)
        return render(request, 'users/index.html', {'users': users, 'id': request.user.id, 'isAdmin': profile.role == 'admin'})
    else:
        return render(request, 'users/index.html', {'users': users, 'id': None})

def showUsers(request, user, messages=None):
    #Si hay un usuario logueado
    if  request.user.is_authenticated:
        #Obtiene el usuario de la base de datos
        user_model = User.objects.get(id=user)
        user_model = Profile.objects.get(user=user)
        
        if messages is None and request.session.get('messages') is not None:
            messages = request.session.get('messages')
            del request.session['messages']
        
        #Redirige el usuario a la vista show
        return render(request, 'users/show.html', {'user_model': user_model, 'messages': messages, 'isAdmin': user_model.role == 'admin'})
    else:
        return redirect('users.index')

def editUsers(request, user):
    #Si el usuario actual es el mismo que el que se quiere editar
    if request.user.id == user:
        #Obtiene el usuario de la base de datos
        user = User.objects.get(id=user)
        profile = Profile.objects.get(user=user)
        
        if request.method == 'POST':
            
            messages = []
            #Actualiza los datos del usuario
            if request.POST['name'] != '':
                profile.name = request.POST['name']
            else:
                messages.append('El nombre no puede estar vacío')

            profile.twitter = request.POST['twitter']
            profile.instagram = request.POST['instagram']
            profile.twitch = request.POST['twitch']

            if request.POST['birthday']:
                profile.birthday = request.POST['birthday']
            else:
                profile.birthday = None
            
            #Comprueba que la contraseña no este vacia y si coincide con la contraseña de confirmacion la guarda
            if request.POST['password'] != '' and request.POST['password'] == request.POST['password_confirmation']:
                profile.password = request.POST['password']
            #Se intenta guardar el usuario

            profile.save()
            
            if len(messages) > 0:
                return render(request, 'users/edit.html', {'user_model': profile, 'user': user, 'messages': messages, 'isAdmin': profile.role == 'admin'})
            #Se le pasa a la vista de show el id del usuario 
            request.session['messages'] = ['Usuario actualizado correctamente']
            return redirect('users.show', profile.id_user)
        
        #Envia el usuario a la vista
        return render(request, 'users/edit.html', {'user_model': profile, 'user': user, 'isAdmin': profile.role == 'admin'})
    else:
        #Si no es el mismo usuario, redirecciona a la pagina de inicio
        return redirect('users.index')
