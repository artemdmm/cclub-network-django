from django.contrib.auth.forms import AuthenticationForm

from .models import User
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password',)