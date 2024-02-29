from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api/register', views.RegisterView.as_view()),
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/getuser', views.UserView.as_view()),
    path('api/getpermissions', views.UserViewWithPerms.as_view()),
    path('api/getuuid', views.RoomView.as_view())
]