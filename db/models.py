from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Videos(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='static/videos/')
    thumbnail = models.ImageField(upload_to='static/thumbnails/')
    description = models.CharField(max_length=250)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Videos, on_delete=models.CASCADE)

class Subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='channel')
