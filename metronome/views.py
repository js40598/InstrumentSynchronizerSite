from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
import numpy as np
from scipy.io.wavfile import write
import os

from InstrumentSynchronizerSite import settings
from InstrumentSynchronizerSite.utils import decode_samples
from metronome.forms import MetronomeCreationForm, MetronomeSaveForm
from metronome.models import Metronome, Tick
from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.Metronome import Metronome as MetronomeFile

# Create your views here.


def about(request):
    return render(request, 'metronome/about.html')


def howto(request):
    return render(request, 'metronome/howto.html')


class Generate(View):
    form = MetronomeCreationForm

    def get(self, request):
        context = {
            'creation_form': self.form(),
        }
        return render(request, 'metronome/generate.html', context)

    def post(self, request):
        context = {
            'creation_form': self.form(initial={'frequency': request.POST['frequency'],
                                                'duration': request.POST['duration'],
                                                'bpm': request.POST['bpm'],
                                                'stereo': request.POST.get('stereo', False),
                                                'tick': request.POST['tick']}),
        }

        if 'creation_submit' in request.POST:
            # generate metronome (to develop)
            if request.user is not None:
                context['save_form'] = MetronomeSaveForm(initial={'frequency': request.POST['frequency'],
                                                                  'duration': request.POST['duration'],
                                                                  'bpm': request.POST['bpm'],
                                                                  'tick': request.POST['tick']})

                metronome_tick_values = np.array(decode_samples(Tick.objects.get(title=request.POST['tick']).values))

                metronome_name = 'Metronome{}Hz{}sec{}bpm{}{}.wav'.format(request.POST['frequency'],
                                                                          request.POST['duration'],
                                                                          request.POST['bpm'],
                                                                          request.POST.get('stereo', False),
                                                                          request.POST['tick'])
                if os.path.exists(metronome_name):
                    pass
                else:
                    generated_metronome = MetronomeFile(frequency=int(request.POST['frequency']),
                                                        duration=int(request.POST['duration']),
                                                        bpm=int(request.POST['bpm']),
                                                        tick_values=metronome_tick_values,
                                                        stereo=request.POST.get('stereo', False))
                    write(metronome_name, generated_metronome.frequency, generated_metronome.samples)
                context['generated_metronome_url'] = metronome_name

            return render(request, 'metronome/generate.html', context)
        elif 'save_submit' in request.POST:
            # save metronome (to develop)
            metronome = Metronome(title=request.POST['title'],
                                  user=request.user,
                                  frequency=request.POST['frequency'],
                                  duration=request.POST['duration'],
                                  bpm=request.POST['bpm'],
                                  tick=Tick.objects.get(title=request.POST['tick']),
                                  stereo=request.POST['stereo'])

        return render(request, 'metronome/generate.html', context)


class Metronomes(View):
    def get(self, request):
        return render(request, 'metronome/generate.html')

    def post(self, request):
        return render(request, 'metronome/generate.html')
