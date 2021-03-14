from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Tick(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='ticks/')
    values = models.TextField()


class Metronome(models.Model):
    POSSIBLE_FREQUENCIES = [('8000', 8000),
                            ('11025', 11025),
                            ('12000', 12000),
                            ('16000', 16000),
                            ('22050', 22050),
                            ('24000', 24000),
                            ('32000', 32000),
                            ('44100', 44100),
                            ('48000', 48000)]
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    frequency = models.CharField(max_length=5, choices=POSSIBLE_FREQUENCIES)
    duration = models.PositiveIntegerField()
    bpm = models.PositiveIntegerField()
    tick = models.ForeignKey(Tick, on_delete=models.DO_NOTHING)
    stereo = models.BooleanField(default=False)

    class Meta:
        unique_together = [['user', 'title'], ['user', 'frequency', 'duration', 'bpm', 'tick', 'stereo']]
