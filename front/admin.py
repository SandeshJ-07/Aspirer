from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostImages)
admin.site.register(Story)
admin.site.register(ChatRoom)
admin.site.register(ChatMsg)