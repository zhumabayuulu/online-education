from django import forms

from blog_nature.models import Nature



class NatureForm(forms.ModelForm):
    class Meta:
        model = Nature
        fields = ('category','address','image','video')

