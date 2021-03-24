from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import NumberInput

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


class CutRecordingForm(forms.Form):
    cut_index = forms.IntegerField()

    def __init__(self, max_value, min_value='0', value='0', *args, **kwargs):
        self.value = value
        self.max_value = max_value
        super(CutRecordingForm, self).__init__(*args, **kwargs)
        self.fields['cut_index'].widget = NumberInput(attrs={'type': 'range',
                                                             'min': '0',
                                                             'max': self.max_value,
                                                             'value': self.value})

    def clean(self):
        if not 0 <= int(self.value) <= int(self.max_value):
            message = 'Provided value is out of expected range'
            raise ValidationError(message)
        return True
