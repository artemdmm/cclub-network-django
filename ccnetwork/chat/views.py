import json
from datetime import datetime

import jwt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.decorators import action
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework.response import Response

from .models import Room, Message
from .serializers import MessageSerializer
from core.models import User

from ccnetwork.settings import SIMPLE_JWT


# Create your views here.
def open_room(request, uuid):
    try:
        room = Room.objects.filter(client=request.user.username).first()
        user_uuid = room.uuid
    except:
        user_uuid = ""
    if request.user.is_staff == True or user_uuid == uuid:
        room = Room.objects.get(uuid=uuid)
        return render(request, 'chat/room.html', {
            'room': room
        })
    else:
        raise PermissionDenied()

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    @action(methods=['get'], detail=False)
    def get(self, request, uuid):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
            user = User.objects.filter(id=payload['id']).first()
            try:
                room = Room.objects.filter(client=user.username).first()
                user_uuid = room.uuid
            except:
                user_uuid = ""
            if not user.is_staff and user_uuid != uuid:
                raise PermissionDenied('Not staff')
        except Exception as e:
            raise AuthenticationFailed(e)

        room = Room.objects.get(uuid=uuid)
        data = room.messages.values('id', 'sent_by', 'body', 'created_at').all()
        return Response(data)

@require_POST
def create_room(request, uuid):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        user = User.objects.filter(id=payload['id']).first()
        if not user.is_staff:
            raise PermissionDenied('Not Staff')
    except:
        raise AuthenticationFailed('Unauthenticated')

    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})

def admin(request):
    if request.user.is_staff:
        rooms = Room.objects.all()

        return render(request, 'chat/admin.html', {
            'rooms': rooms
        })
    else:
        raise PermissionDenied('Not Staff')

def rooms_api(request):
    token = request.COOKIES.get('jwt')
    if not token:
        raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        user = User.objects.filter(id=payload['id']).first()
        if not user.is_staff:
            raise AuthenticationFailed('Not Staff')
    except:
        raise AuthenticationFailed('Unauthenticated')

    rooms = Room.objects.all()
    data = []
    for room in rooms:
        data.append({
            'uuid': room.uuid,
            'client': room.client,
            'status': room.status
        })
    print(data)
    return JsonResponse(data, safe=False)

def status_update(request):
    token = request.COOKIES.get('jwt')
    if not token:
        if not request.user.is_authenticated:
            raise AuthenticationFailed('Unauthenticated')
    try:
        payload = jwt.decode(token, SIMPLE_JWT['SIGNING_KEY'], algorithms=[SIMPLE_JWT['ALGORITHM']])
        user = User.objects.filter(id=payload['id']).first()
        if not user.is_staff or not request.user.is_staff:
            raise PermissionDenied('Not Staff')
    except:
        if not request.user.is_authenticated:
            raise AuthenticationFailed('Unauthenticated')

    uuid = request.POST.get('uuid', '')
    status = request.POST.get('status', '')

    obj = Room.objects.get(uuid=uuid)
    if status == 'waiting':
        obj.status = Room.WAITING
    elif status == 'active':
        obj.status = Room.ACTIVE
    elif status == 'closed':
        obj.status = Room.CLOSED
    obj.save()

    return JsonResponse({'message': obj.status})