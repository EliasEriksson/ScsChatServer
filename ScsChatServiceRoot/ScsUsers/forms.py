from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    """
    registration where only username and password is required.
    """
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
