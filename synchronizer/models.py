from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=200, blank=True)
    creation_date = models.DateField(editable=False, blank=True)
    edition_date = models.DateTimeField(blank=True)

    # set dates on creation or saving
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.now()
        self.edition_date = datetime.now()
        return super(Project, self).save(*args, **kwargs)

    class Meta:
        unique_together = [['user', 'title']]


class Recording(models.Model):
    project = models.ForeignKey(Project, related_name='recordings', on_delete=models.CASCADE)
    file = models.FileField(upload_to='recordings/')
    instrument = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, blank=True)
    pitch = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    samples = models.TextField()
