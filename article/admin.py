from django.contrib import admin
from .models import Post, Subscriber, Rating

# Register your models here.

admin.site.register(Post)
admin.site.register(Subscriber)
admin.site.register(Rating)