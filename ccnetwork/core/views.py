import datetime
import jwt
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User
from .serializers import UserSerializer
from chat.models import Room


# Create your views here.
def index(request):
    return render(request, 'core/index.html')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found!')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password!')

        user = authenticate(username=username, password=password)

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }
        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

class UserViewWithPerms(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()

        try:
            room = Room.objects.filter(client=user.username).first()
            uuid = room.uuid
        except:
            uuid = ""

        response = Response()

        if user.is_staff:
            response.data = {
                'id': user.id,
                'username': user.username,
                'permissions': True,
                'uuid': uuid
            }
        else:
            response.data = {
                'id': user.id,
                'username': user.username,
                'permissions': False,
                'uuid': uuid
            }
        return response

class PermissionsView(APIView):
    def get(self, request):
        try:
            username = request.data['username']
            user = User.objects.get(username=username)
        except:
            raise AuthenticationFailed('User not found!')

        response = Response()
        if user.is_staff:
            response.data = {
                'permissions': True
            }
        else:
            response.data = {
                'permissions': False
            }
        return response

class RoomView(APIView):
    def get(self, request):
        response = Response()
        try:
            username = request.data['username']
            room = Room.objects.filter(client=username).first()
            response.data = {
                'UUID': room.uuid
            }
            return response
        except:
            raise AuthenticationFailed('Room not found!')
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response