from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Tick(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='ticks/')
    values = models.TextField()


class Metronome(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    frequency = models.PositiveIntegerField()
    duration = models.PositiveIntegerField()
    bpm = models.PositiveIntegerField()
    tick = models.ForeignKey(Tick, on_delete=models.DO_NOTHING)
    stereo = models.BooleanField(default=False)
