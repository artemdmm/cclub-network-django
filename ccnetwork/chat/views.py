from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework import generics
from rest_framework.response import Response

from .models import Room, Message
from .serializers import MessageSerializer

# Create your views here.
def open_room(request, uuid):
    room = Room.objects.get(uuid=uuid)
    return render(request, 'chat/room.html', {
        'room': room
    })

class MessageList(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        uuid = self.kwargs['uuid']
        room = Room.objects.get(uuid=uuid)
        return room.messages.all()

@require_POST
def create_room(request, uuid):
    name = request.POST.get('name', '')
    url = request.POST.get('url', '')

    Room.objects.create(uuid=uuid, client=name, url=url)

    return JsonResponse({'message': 'room created'})

def admin(request):
    rooms = Room.objects.all()

    return render(request, 'chat/admin.html', {
        'rooms': rooms
    })

def rooms_api(request):
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