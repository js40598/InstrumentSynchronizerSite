from django.contrib.auth.models import User
from django.db import models
from datetime import datetime

# Create your models here.


class Project(models.Model):
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    creation_date = models.DateField(editable=False)
    edition_date = models.DateTimeField()

    # set dates on creation or saving
    def save(self, *args, **kwargs):
        if not self.id:
            self.creation_date = datetime.now()
        self.edition_date = datetime.now()
        return super(Project, self).save(*args, **kwargs)


class Recording(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='recordings/')
    instrument = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, blank=True)
    pitch = models.CharField(max_length=100, blank=True)
    author = models.CharField(max_length=100, blank=True)
    samples = models.TextField()
