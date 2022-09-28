
from datetime import datetime
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UserName','class': 'form-control'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'lable':'Password Confirmation','placeholder': 'Password Confirmation','class': 'form-control'}), label='Password Confirmation')

    class Meta:
        model = User  # this is the "YourCustomUser" that you imported at the top of the file
        fields = ('username', 'email', 'password1', 'password2')

        
    def get_user(self):
        return authenticate(
                username = self.cleaned_data.get('username', '').lower().strip(),
                password = self.cleaned_data.get('password2', ''),
        )        


class LoginForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'UserName','class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'form-control'}), label='Password')
    class Meta:
        model = User
        fields = ('username', 'password')


    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Incorrect Username / Password please try again.")


    def get_user(self):
   
        return authenticate(
                username = self.cleaned_data.get('username').lower().strip(),
                password = self.cleaned_data.get('password'),
        )        

