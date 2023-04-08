from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, ContactForm


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ("username", "email",)

class  CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = ("username", "first_name", "last_name", "pic", 'bio','birthday','address','phone_number')

class ContactFormm(forms.ModelForm):
    class Meta :
        model = ContactForm
        fields ='name','message','email'