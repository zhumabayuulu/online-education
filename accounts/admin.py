

from django.contrib import admin
from .models import CustomUser, Friend, ContactForm


# Register your models here.
admin.site.register(CustomUser)

admin.site.register(Friend)

admin.site.register(ContactForm)
