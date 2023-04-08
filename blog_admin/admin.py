from django.contrib import admin

# Register your models here.
from blog_admin.models import AdminCategory, AlmanAdmin

admin.site.register(AlmanAdmin)
admin.site.register(AdminCategory)