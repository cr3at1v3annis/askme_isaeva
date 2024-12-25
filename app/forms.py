from django import forms
from app import models
from django.contrib import auth


class LoginForms(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        data = super().clean()
        username = data.get('username')

        if username != username.lower():
            self.add_error('username', 'Username must be lowercased.')

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label="Nickname", max_length=30, min_length=3)
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput(), max_length=80, min_length=6)
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password'}), max_length=80, min_length=6)

    class Meta:
        model = models.Profile
        fields = ["username", "email", "password",
                  "confirm_password", "avatar"]

    def save(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.pop('confirm_password')
        if password != confirm_password:
            self.add_error(
                field=None, error="Password and the confirmation password do not match")
            return False

        email = self.cleaned_data.get('email')
        if auth.models.User.objects.filter(email=email):
            self.add_error(field=None, error="This email already exist")
            return False

        username = self.cleaned_data.get('username')
        if auth.models.User.objects.filter(username=username):
            self.add_error(field=None, error="This nickname already exist")
            return False

        avatar = self.cleaned_data.pop('avatar')
        try:
            user = auth.models.User.objects.create_user(**self.cleaned_data)
            models.Profile.objects.create(
                user=user,
                avatar=avatar)
        except Exception as e:
            self.add_error(field=None, error="Error")
            return False
        return self.cleaned_data
