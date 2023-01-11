from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)


class Message(models.Model):
    value = models.CharField(max_length=10000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    channel = models.ForeignKey(Room, on_delete=models.CASCADE)
