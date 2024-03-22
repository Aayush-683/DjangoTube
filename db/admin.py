from django.contrib import admin
from .models import *

# Register your models here.
models = [User, Videos, Likes, Subscriptions]
admin.site.register(models)