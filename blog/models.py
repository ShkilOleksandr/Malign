from django.db import models
from django.contrib.auth.models import User, AbstractUser

from Malign import settings


class Creator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    website = models.URLField(blank=True, null=True)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class Podcast(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE)
    link = models.URLField()
    description = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to='images/')

class Comment(models.Model):
    post = models.ForeignKey('Podcast', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField()


