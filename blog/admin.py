from django.contrib import admin
from .models import Podcast, Creator, CustomUser
from .models import Comment
admin.site.register(Podcast)
admin.site.register(Comment)
admin.site.register(Creator)
admin.site.register(CustomUser)