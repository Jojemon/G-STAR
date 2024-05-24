from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseForbidden
from .models import Room, Message, Profile
from .forms import RoomCreationForm, MessageForm, CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            role = form.cleaned_data.get('role')
            section = form.cleaned_data.get('section')

            user = authenticate(username=username, password=password)
            login(request, user)

            # Set the user's profile role and section based on the selected role in the form
            profile = Profile.objects.get(user=user)
            profile.role = role
            profile.section = section
            profile.save()

            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')


@login_required

def index(request):
    try:
        user_profile = request.user.profile
        print(f"User: {request.user.username}, Role: {user_profile.role}, Section: {user_profile.section}")

        if user_profile.role == 'student':
            rooms = Room.objects.filter(section=user_profile.section)
        else:  # For teachers, show only rooms they created
            rooms = Room.objects.filter(created_by=request.user)

        print(f"Rooms: {rooms}")
    except Exception as e:
        print(f"Error: {e}")
        rooms = []

    return render(request, 'index.html', {'rooms': rooms})

@login_required
def group_chat(request):
    if request.user.profile.role == 'student':
        rooms = Room.objects.filter(section=request.user.profile.section)
    else:  # Teacher
        rooms = Room.objects.filter(created_by=request.user)
    return render(request, 'group_chat.html', {'rooms': rooms})

@login_required
def create_room(request):
    if request.user.profile.role != 'teacher':
        return HttpResponseForbidden("You must be a teacher to create a room.")

    if request.method == 'POST':
        form = RoomCreationForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.created_by = request.user
            room.save()
            return redirect('group_chat')
    else:
        form = RoomCreationForm()
    return render(request, 'create_room.html', {'form': form})

def chat_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    if request.user.profile.role == 'student' and request.user.profile.section != room.section:
        return HttpResponseForbidden("You do not have permission to view this room.")

    messages = Message.objects.filter(room=room).order_by('id')
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            content = message_form.cleaned_data['content']
            sender = request.user
            Message.objects.create(content=content, room=room, sender=sender)
            return redirect('chat_room', room_id=room_id)
    else:
        message_form = MessageForm()

    return render(request, 'chat_room.html', {'room': room, 'messages': messages, 'message_form': message_form})
