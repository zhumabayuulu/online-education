from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ContactForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username","password1","password2")
        labels = {
            'username':"Колдонуучунун аты ",
        }

class  CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ("username", "first_name","pic", 'bio','phone_number')

class ContactFormm(forms.ModelForm):
    class Meta :
        model = ContactForm
        fields ='name','message','email'