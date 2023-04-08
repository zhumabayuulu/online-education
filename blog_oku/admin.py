from django.contrib import admin

# Register your models here.
from blog_oku.models import *


class QuestionInline(admin.TabularInline):
    model = Question


class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline, ]
    list_display = ['title', 'author']


# test

admin.site.register([TestCategory, Question]),
admin.site.register(Test, TestAdmin),
admin.site.register([CheckTest,CheckQuestion])

# endtest

# bloglearn

admin.site.register(BlogLearn)
admin.site.register(BlogLearnComment)
admin.site.register(LearnCategory)
