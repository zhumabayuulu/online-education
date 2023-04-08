from django.contrib import admin

# Register your models here.
from blog_nature.models import NatureCategory, Nature, Like



class NatureAdmin(admin.ModelAdmin):
    list_display = ['id', "date", 'category', "author"]


admin.site.register(Nature,NatureAdmin),
admin.site.register(NatureCategory),
admin.site.register(Like)
