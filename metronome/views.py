import os

import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from scipy.io.wavfile import write

from InstrumentSynchronizerSite import settings
from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.AudioFile import AudioFile
from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.Metronome import Metronome as MetronomeFile
from InstrumentSynchronizerSite.utils import decode_samples
from metronome.forms import MetronomeCreationForm, MetronomeSaveForm
from metronome.models import Metronome, Tick


# Create your views here.


def about(request):
    return render(request, 'metronome/about.html')


def howto(request):
    return render(request, 'metronome/howto.html')


def download_metronome(request, metronome_name):
    if request.method == 'POST':
        with open(os.path.join(Generate.output_dir, metronome_name), 'rb') as file:
            response = HttpResponse(file.read(), content_type="application/wav")
            response['Content-Disposition'] = 'inline; filename=' + metronome_name
            return response


class Generate(View):
    form = MetronomeCreationForm
    output_dir = os.path.join(settings.BASE_DIR, 'InstrumentSynchronizerSite', 'static', 'metronomes')

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

        if 'creation_submit' in request.POST or 'download_submit' in request.POST:
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
                                                                          request.POST.get('stereo', ''),
                                                                          request.POST['tick'])
                metronome_url = os.path.join(settings.BASE_DIR,
                                             'InstrumentSynchronizerSite',
                                             'static',
                                             'metronomes',
                                             metronome_name)
                if os.path.exists(metronome_url):
                    pass
                else:
                    generated_metronome = MetronomeFile(frequency=int(request.POST['frequency']),
                                                        duration=int(request.POST['duration']),
                                                        bpm=int(request.POST['bpm']),
                                                        tick_values=metronome_tick_values,
                                                        stereo=request.POST.get('stereo', False))
                    write(metronome_url, generated_metronome.frequency, generated_metronome.samples)
                a = AudioFile(metronome_url)
                a.convert('mp3', True)
                metronome_name = metronome_name[:-3] + a.format
                context['generated_metronome_name'] = metronome_name
                context['generated_metronome_url'] = a.directory

            return render(request, 'metronome/generate.html', context)
        elif 'save_submit' in request.POST:
            # save metronome (to develop)
            metronome = Metronome(title=request.POST['title'],
                                  user=request.user,
                                  frequency=request.POST['frequency'][1],
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
