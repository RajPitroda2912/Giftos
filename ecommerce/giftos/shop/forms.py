from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class RegisterUser(UserCreationForm):
    name = forms.CharField(required=True,label='Username',widget=forms.TextInput(
        attrs={'class':'form-control','placeholder':'Enter your Username'}))
    email = forms.EmailField(label='Email',widget=forms.EmailInput(
        attrs={'class':'form-control','placeholder':'Enter your Email'}))
    password1 = forms.CharField(required=True,label='Password',widget=forms.TextInput(
        attrs={'class':'form-control','type':'password','placeholder':'Enter your Password'}))
    password2 = forms.CharField(required=True,label='Confirm Password',widget=forms.TextInput(
        attrs={'class':'form-control','type':'password','placeholder':'Enter your Confirm Password'}))
    captcha = ReCaptchaField(required=True, label='Captcha', widget=ReCaptchaV2Checkbox)

    class Meta:
        model = user
        fields = ['name', 'email', 'password1', 'password2']

    def __str__(self):
        return self.name 
    
class ReCaptcha(forms.Form):
    captcha = ReCaptchaField(required=True, label='Captcha', widget=ReCaptchaV2Checkbox)