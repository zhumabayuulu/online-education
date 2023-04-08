from django.db import models

# Create your models here.
from accounts.models import CustomUser


class Chat(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='receiver')
    chat = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
    is_seen = models.CharField(default="&#10003;", max_length=150)


    def __str__(self):
        return str(self.sender) + ' >>> ' + str(self.receiver)
