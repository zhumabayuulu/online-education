from django.db import models

# Create your models here.
from accounts.models import CustomUser


class AdminCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class AlmanAdmin(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(AdminCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    photo = models.ImageField(upload_to='media/images/', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(CustomUser, default=None, blank=True, related_name='like_admin')


    def __str__(self):
        return str(self.author)
    class Meta:
        ordering = ('-id',)

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class LikeAdmin(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(AlmanAdmin, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)

    def __str__(self):
        return str(self.post)