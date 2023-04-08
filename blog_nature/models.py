from django.db import models

# Create your models here.
from accounts.models import CustomUser
from .validators import file_size


class NatureCategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Nature(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, )
    category = models.ForeignKey(NatureCategory, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    video = models.FileField(upload_to="video/%y", blank=True, null=True, validators=[file_size])
    image = models.ImageField(upload_to='product_images',blank=True, null=True,)
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(CustomUser, default=None, blank=True, related_name='liked')

    @property
    def num_likes(self):
        return self.liked.all().count()

    def __str__(self):
        return str(self.category)

    class Meta:
        ordering = ('-id',)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Nature, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)

    def __str__(self):
        return str(self.post)

