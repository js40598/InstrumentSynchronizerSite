from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Metronome, Tick


class MetronomeCreationForm(forms.ModelForm):
    TICK_CHOICES = [(tick.id, tick) for tick in Tick.objects.all()]

    class Meta:
        model = Metronome
        fields = ['frequency', 'duration', 'bpm', 'stereo', 'tick']

    def __init__(self, *args, **kwargs):
        super(MetronomeCreationForm, self).__init__(*args, **kwargs)
        self.fields['tick'].widget = forms.RadioSelect(choices=self.TICK_CHOICES)


class MetronomeSaveForm(forms.ModelForm):
    class Meta:
        model = Metronome
        fields = ['title', 'frequency', 'duration', 'bpm', 'tick', 'stereo', 'user']
        widgets = {'frequency': forms.HiddenInput(),
                   'duration': forms.HiddenInput(),
                   'bpm': forms.HiddenInput(),
                   'tick': forms.HiddenInput(),
                   'stereo': forms.HiddenInput(),
                   'user': forms.HiddenInput(),
                   }

    def clean(self):
        query = Metronome.objects.filter(user=User.objects.get(username=self.cleaned_data.get('user')),
                                         title=self.cleaned_data.get('title'))
        if len(query) > 0:
            message = 'Metronome with this title already exists'
            raise ValidationError(message)
        query = Metronome.objects.filter(user=User.objects.get(username=self.cleaned_data.get('user')),
                                         frequency=self.cleaned_data.get('frequency'),
                                         duration=self.cleaned_data.get('duration'),
                                         bpm=self.cleaned_data.get('bpm'),
                                         tick=self.cleaned_data.get('tick'),
                                         stereo=self.cleaned_data.get('stereo'))
        if len(query) > 0:
            message = 'This metronome already exists with different title'
            raise ValidationError(message)
        return self.cleaned_data
