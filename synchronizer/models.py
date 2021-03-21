from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from InstrumentSynchronizerSite.utils import random_ascii_string

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
    file = models.FileField(upload_to='recordings/')
    instrument = models.CharField(max_length=100, blank=True)
    identifier = models.CharField(max_length=100)
    slug = models.SlugField(blank=True)
    pitch = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    samples = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        slug = slugify(self.instrument + self.identifier)
        slug_list = [recording.slug for recording in self.project.recordings.all()]
        while slug in slug_list:
            slug = slugify('{}-{}-{}'.format(self.instrument, self.identifier, random_ascii_string(5)))
        self.slug = slug
        return super(Recording, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['project', 'identifier']]
