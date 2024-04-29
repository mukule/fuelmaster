from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import PasswordResetForm
from .models import *
from django.contrib.auth.forms import UserChangeForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        help_text='A valid email address, please.', required=True)

    ACCESS_LEVEL_CHOICES = CustomUser.ACCESS_LEVEL_CHOICES

    access_level = forms.ChoiceField(
        choices=ACCESS_LEVEL_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', 'access_level', 'branch']

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)

        # Add CSS classes to form fields
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Email Address'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['access_level'].widget.attrs.update(
            {'class': 'form-control'})
        self.fields['branch'].widget.attrs.update(
            {'class': 'form-control'})

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.access_level = self.cleaned_data['access_level']
        user.branch = self.cleaned_data['branch']

        if commit:
            user.save()
        return user


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control border-end-0',
               'placeholder': 'Password',
               'id': 'inputChoosePassword'}),  # Add 'id' attribute here
        label="")


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']


class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, required=False)
    is_active = forms.BooleanField(required=False)
    access_level = forms.ChoiceField(
        choices=get_user_model().ACCESS_LEVEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password',
                  'confirm_password', 'access_level', 'is_active']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user
