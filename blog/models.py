from django.db import models
from django.contrib.auth.models import User, AbstractUser

from Malign import settings


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.username

class Creator(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='creator_profile')
    bio = models.TextField(blank=True, default='')
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Creator: {self.user.username}"

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
    author = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    pub_date = models.DateTimeField()


