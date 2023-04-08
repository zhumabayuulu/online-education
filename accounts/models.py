from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.CharField(max_length=100, null=True, blank=True)
    pic = models.ImageField(upload_to='profiles/', default="photo/avatar.svg")
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)


class Friend(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friend')
    unread = models.PositiveIntegerField(default=0, )

    def __str__(self):
        return str(self.friend)


# save nature
class SavedNature(models.Model):
    nature = models.ForeignKey("blog_nature.Nature", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return "Comment of " + str(self.author)


# saved product
class Saved(models.Model):
    product = models.ForeignKey("store.Product", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)


    def __str__(self):
        return "Comment of " + str(self.author)


class SavedAdmin(models.Model):
    almanadmin = models.ForeignKey("blog_admin.AlmanAdmin", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Comment of " + str(self.author)


class SavedLearn(models.Model):
    bloglearn = models.ForeignKey("blog_oku.BlogLearn", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Comment of " + str(self.author)


class SavedTest(models.Model):
    test = models.ForeignKey("blog_oku.Test", on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return "Comment of " + str(self.author)


# contact form
class ContactForm(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.email
