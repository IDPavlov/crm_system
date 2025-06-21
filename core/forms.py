from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile
from crispy_forms.helper import FormHelper

class CustomUserCreationForm(UserCreationForm):
    secret_key = forms.CharField(
        required=False,
        label="Analyst Secret Key",
        help_text="Enter secret key to register as analyst"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'secret_key')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'avatar', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True