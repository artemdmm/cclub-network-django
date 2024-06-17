from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from rest_framework.permissions import IsAuthenticated

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('api/register', views.RegisterView.as_view()),
    path('api/login', views.LoginView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('api/getuser', views.UserView.as_view()),
    path('api/getpermissions', views.UserViewWithPerms.as_view()),
    path('api/getuuid', views.RoomView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
]