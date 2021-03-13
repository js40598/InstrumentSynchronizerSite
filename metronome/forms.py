from django import forms
from .models import Metronome, Tick


class MetronomeCreationForm(forms.ModelForm):
    TICK_CHOICES = [(tick.title, tick.title) for tick in Tick.objects.all()]

    frequency = forms.ChoiceField(choices=Metronome.POSSIBLE_FREQUENCIES)
    tick = forms.ChoiceField(choices=TICK_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Metronome
        fields = ['frequency', 'duration', 'bpm', 'tick', 'stereo']


class MetronomeSaveForm(forms.ModelForm):
    class Meta:
        model = Metronome
        fields = ['title', 'frequency', 'duration', 'bpm', 'tick', 'stereo', 'user']
        widgets = {
                   'duration': forms.HiddenInput(),
                   'bpm': forms.HiddenInput(),
                   'tick': forms.HiddenInput(),
                   'stereo': forms.HiddenInput(),
                   'user': forms.HiddenInput(),
                   }
