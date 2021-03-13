from django import forms
from .models import Metronome, Tick


class MetronomeCreationForm(forms.ModelForm):
    class Meta:
        model = Metronome
        fields = ['frequency', 'duration', 'bpm', 'tick', 'stereo']


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
