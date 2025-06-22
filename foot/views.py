from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .form import RoomForm, UserForm
from django.contrib import messages
# foot is our base app.

# rooms = [
#     {'id':1, 'name':'Lets learn python'},
#     {'id':2, 'name':'Lets learn Calculus'},
#     {'id':3, 'name':'Lets learn Algebra'},
# ]
# creating the methods to render pages.

def loginPage(request):

    page = 'login'
    # the below condition is very specifc one to handle direct url access to loginpage!!!
    if request.user.is_authenticated:
        return redirect('home')


    if request.method == "POST":
        username = request.POST.get('username', '').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'user does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')

        else:
            messages.error(request, 'username or password does not exist')

    context= {'page':page}
    return render(request, 'foot/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'foot/login_register.html', {'form':form})

def Home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    # rooms = Room.objects.all()
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) | 
        Q(name__icontains=q) | 
        Q(description__icontains=q)
    )
    
    
    topics = Topic.objects.all()
    room_count = rooms.count()

    # for feed activity
    # we have also fileters out the quick messages clicks to reflect 
    # the feeds based on the topics we click to search
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))


    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count,
               'room_messages':room_messages}
    return render(request, 'foot/home.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()

    # getting the all the participants
    participants = room.participants .all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        # functionality to add the participants
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room':room, 'room_messages':room_messages, 'participants':participants}
    return  render(request, 'foot/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()

    context = {'user': user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'foot/profile.html', context )
# created a method to request form from room_form.html
# then go to foot/urls.py

@login_required(login_url= 'login') #maing sure we let user to create the room if the user is logedin
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    # making sure of the form submission
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')

        )
        
        # form= RoomForm(request.POST)
        # if form.is_valid():
            # the host will be set based on login
            # room = form.save(commit=False)
            # room.host = request.user
            # form.save()
        return redirect('home')
        
        # print(request.POST)
    context = {'form':form, 'topics':topics}
    return render(request, 'foot/room_form.html', context)


@login_required(login_url= 'login') #making sure we let user to update the room if the user is logedin
def updateRoom(request, pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
# making sure usesr is only allowed tp update if it is logedin/Authaurized 
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')

# making sure of the form submission
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()

        return redirect('home')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'foot/room_form.html', context)

@login_required(login_url= 'login')#maing sure we let user to delete the room if the user is logedin
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    # making sure user is only allowed to delete if it is logedin/Authaurized 
    if request.user != room.host:
        return HttpResponse('You are not allowed here!!')
    
    # making sure of the form submission
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'foot/delete.html', {'obj':room})


# funtionm to allow a user to delete the message
@login_required(login_url= 'login')#maing sure we let user to delete the room if the user is logedin
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    # making sure user is only allowed to delete if it is logedin/Authaurized 
    if request.user != message.user:
        return HttpResponse('You are not allowed here!!')
    
    # making sure of the form submission
    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'foot/delete.html', {'obj':message})


    # addin an update user function
@login_required(login_url= 'login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST,instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'foot/update-user.html', {'form':form})


# functions specific for mobile view
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'foot/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'foot/activity.html', {'room_messages': room_messages})