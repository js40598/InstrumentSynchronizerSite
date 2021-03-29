from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.AudioFile import AudioFile
from InstrumentSynchronizerSite.utils import random_ascii_string
import os
from InstrumentSynchronizerSite.settings import RECORDINGS_URL
from InstrumentSynchronizerSite import settings
import numpy as np

from django.utils.text import slugify

from metronome.models import PositiveIntegerRangeField

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, blank=True)
    bpm = PositiveIntegerRangeField(min_value=10, max_value=300)
    creation_date = models.DateField(editable=False, blank=True)
    edition_date = models.DateTimeField(blank=True)

    # set dates on creation or saving
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.now()
            self.slug = slugify(self.title)
        self.edition_date = datetime.now()
        return super(Project, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['user', 'title']]


class Recording(models.Model):
    project = models.ForeignKey(Project, related_name='recordings', on_delete=models.CASCADE)
    file = models.FileField(upload_to='InstrumentSynchronizerSite/static/recordings')
    first_beat_index = models.IntegerField(blank=True)
    instrument = models.CharField(max_length=100, blank=True)
    identifier = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    pitch = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    samples = models.TextField(blank=True)
    cut = models.BooleanField(default=False)
    synchronized = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.cut and not self.synchronized:
            recordings = Recording.objects.filter(project=self.project)
            if len(recordings) > 0:
                index_difference = recordings[0].first_beat_index - self.first_beat_index
                if index_difference > 0:
                    file_directory = os.path.join(settings.RECORDINGS_ROOT, self.file.name)
                    audio_file = AudioFile(file_directory)
                    samplesleft = list(audio_file.samplesleft)
                    samplesright = list(audio_file.samplesright)
                    audio_file.samplesleft = np.array(samplesleft[0] * index_difference + samplesleft)
                    audio_file.samplesright = np.array(samplesright[0] * index_difference + samplesright)
                    audio_file.save_file()
                    self.first_beat_index = recordings[0].first_beat_index
                elif index_difference < 0:
                    for recording in recordings:
                        file_directory = os.path.join(settings.RECORDINGS_ROOT, recording.file.name)
                        audio_file = AudioFile(file_directory)
                        audio_file.samplesleft = np.array([0] * abs(index_difference) + list(audio_file.samplesleft))
                        audio_file.samplesright = np.array([0] * abs(index_difference) + list(audio_file.samplesright))
                        audio_file.save_file()
                        recording.first_beat_index = self.first_beat_index
                        recording.save()
                self.synchronized = True

        slug = slugify(self.instrument + self.identifier)
        slug_list = [recording.slug for recording in self.project.recordings.all()]
        while slug in slug_list:
            slug = slugify('{}-{}-{}'.format(self.instrument, self.identifier, random_ascii_string(5)))
        self.slug = slug
        return super(Recording, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['project', 'identifier']]
