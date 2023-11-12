from django.shortcuts import render, redirect
from django.contrib import messages as msg

from .models import Message, Room


def index(request):
    if not request.user.is_authenticated:
        return redirect('account:login_view')
    user = request.user
    user_rooms = Room.objects.filter(is_active=True, room_user_room__user=user)
    return render(request, 'chat/index.html', {'rooms': user_rooms, 'user': user})


def document_view(request):
    return render(request, 'chat/doc.html')


def room(request, room_code):
    if not request.user.is_authenticated:
        return redirect('account:login_view')

    username = request.user.username
    try:
        _room, created = Room.objects.get_or_create(is_active=True, code=room_code)
    except Room.DoesNotExist as e:
        msg.warning(request, "Room not found!")
        return redirect('index')
    chats = Message.objects.filter(user_room__room=_room)[0:25]
    return render(request, 'chat/room.html', {'room_code': _room.code, 'username': username, 'chats': chats})
