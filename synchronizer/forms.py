from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from synchronizer.models import Project, Recording


class ProjectCreationForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ['title', 'description', 'user', 'bpm']


class RecordingAddForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = Recording
        fields = ['file', 'instrument', 'identifier', 'pitch', 'author', 'project']
