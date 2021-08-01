
from django import forms
from .validators import FormValidators
from django.contrib.auth.forms import UserCreationForm
from .choices import TYPE_USER
from user.models import User


class RegisterUserForm(UserCreationForm, forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), validators=[FormValidators.password_validation])
    password2 = forms.CharField(widget=forms.PasswordInput(), validators=[FormValidators.password_validation])
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField(validators=[FormValidators.username_validation])
    email = forms.CharField(validators=[FormValidators.email_validation])
    type_user = forms.ChoiceField(choices=TYPE_USER)

    class Meta:
        model = User
        fields = ("password1", "password2", "first_name", "last_name", "email", "type_user", "username")