
from django.db import models
from accounts.models import CustomUser
class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BookLanguage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Product(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category,  on_delete=models.CASCADE)
    language = models.ForeignKey(BookLanguage, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=100,blank=True,  null=True)
    price = models.IntegerField(blank=True,  null=True)

    book_author = models.CharField(max_length=100, blank=True, )
    pdf = models.FileField(upload_to='books/pdfs/',blank=True,  null=True)
    date = models.DateTimeField(auto_now_add=True)
    liked = models.ManyToManyField(CustomUser, default=None, blank=True, related_name='like_store')

    def __str__(self):
        return str(self.title)

    class Meta:
        ordering = ('-id',)

    @property
    def num_likes(self):
        return self.liked.all().count()



LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class LikeStore(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)

    def __str__(self):
        return str(self.post)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images')




# comment
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.CharField(max_length=150)
    date = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)
    liked = models.ManyToManyField(CustomUser, default=None, blank=True, related_name='like_store_comment')

    def __str__(self):
        return "Comment of " + str(self.author.username)

    @property
    def num_likes(self):
        return self.liked.all().count()


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class LikeStoreComment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Comment, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='like', max_length=10)