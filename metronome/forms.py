from django import forms
from .models import Metronome, Tick


class MetronomeCreationForm(forms.ModelForm):
    # TICK_CHOICES = [(tick.title, tick.title) for tick in Tick.objects.all()]
    TICK_CHOICES = [('a', 'A'), ('b', 'B')]  # temporarily to show anything if Tick table is empty

    tick = forms.ChoiceField(choices=TICK_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Metronome
        fields = ['frequency', 'duration', 'bpm', 'tick', 'stereo']
