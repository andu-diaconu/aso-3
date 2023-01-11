from django.core.files.storage import default_storage
from django.shortcuts import render, redirect
from project import settings

from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


def register(req):
    if req.user.is_authenticated:
        return redirect('root')
    else:
        form = CreateUserForm()

        if req.method == 'POST':
            form = CreateUserForm(req.POST)
            if form.is_valid():
                form.save()
                return redirect('sign in')
            else:
                messages.error(req, list(form.error_messages.values())[0])

        context = {'form': form}
        return render(req, 'register.html', context)


def signin(req):
    if req.user.is_authenticated:
        return redirect('root')
    else:
        if req.method == 'POST':
            username = req.POST.get('username')
            password = req.POST.get('password')

            user = authenticate(req, username=username, password=password)
            if user is not None:
                login(req, user)
                return redirect('root')
            else:
                messages.error(req, 'Incorrect Credentials')

        context = {}
        return render(req, 'login.html', context)


def signout(req):
    logout(req)
    return redirect('sign in')


@login_required(login_url='sign in')
def general(req):
    general_messages = Message.objects.filter(channel_id=1).all()
    current_user = req.user
    return render(req, 'home.html', {'messages': general_messages, 'current_user': current_user.id})


@login_required(login_url='sign in')
def search_room(req):
    channel = req.POST.get('room_name')
    if Room.objects.filter(name=channel).exists():
        return redirect('/'+channel)
    else:
        return redirect('/login')


@login_required(login_url='sign in')
def room(req, channel):
    current_user = req.user
    room_id = get_object_or_404(Room, name=channel).id
    room_messages = Message.objects.filter(channel_id=room_id).all()
    return render(req, 'room.html', {'messages': room_messages, 'current_user': current_user.id, 'channel_name': channel})


def create_room(req):
    return render(req, 'new_room.html', {})


def create(req):
    channel_name = req.POST.get('room_name')
    if Room.objects.filter(name=channel_name).exists():
        return redirect('/'+channel_name)
    else:
        new_room = Room.objects.create(name=channel_name)
        new_room.save()
        subject = channel_name+" room on Chat App"
        body = req.user.username+" just created room ' "+channel_name+" '.He invited you to join."
        str = req.POST.get('emails', '')
        to = str.split(", ")

        send_mail(subject, body, settings.EMAIL_HOST_USER, to)
        return redirect('/'+channel_name)


def send_message(req):
    file = req.FILES.get('img', '')
    if file != '':
        file_name = default_storage.save(file.name, file)
        message = file_name
    else:
        message = req.POST['message']
    user = req.user
    channel = Room.objects.get(name=req.POST['channel'])
    now = datetime.now()

    new_message = Message.objects.create(value=message, author=user, date=now.strftime('%Y-%m-%d %H:%M'), channel=channel)
    new_message.save()
    return HttpResponse('Sent')


def get_messages(req, room):
    current_room = Room.objects.get(name=room)
    messages = Message.objects.filter(channel_id=current_room.id)

    return JsonResponse({"messages": list(messages.values())})
