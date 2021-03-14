import os

import numpy as np
from django.contrib.auth.decorators import login_required
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
        context = {'creation_form': self.form(initial={'frequency': request.POST['frequency'],
                                                       'duration': request.POST['duration'],
                                                       'bpm': request.POST['bpm'],
                                                       'stereo': request.POST.get('stereo', False),
                                                       'tick': request.POST['tick']})}
        metronome_name = 'Metronome{}Hz{}sec{}bpm{}{}.wav'.format(request.POST['frequency'],
                                                                  request.POST['duration'],
                                                                  request.POST['bpm'],
                                                                  'Stereo' if request.POST['stereo'] else '',
                                                                  Tick.objects.get(id=request.POST['tick']).title)
        metronome_url = os.path.join(settings.BASE_DIR,
                                     'InstrumentSynchronizerSite',
                                     'static',
                                     'metronomes',
                                     metronome_name)

        if 'creation_submit' in request.POST:
            validate_form = MetronomeCreationForm(data={'frequency': request.POST['frequency'],
                                                        'duration': request.POST['duration'],
                                                        'bpm': request.POST['bpm'],
                                                        'tick': request.POST['tick'],
                                                        'stereo': True if request.POST.get('stereo') else False})
            if validate_form.is_valid():
                if not os.path.exists(metronome_url[:-3]+'mp3'):
                    if not os.path.exists(metronome_url):
                        selected_tick = Tick.objects.get(id=request.POST['tick'])
                        metronome_tick_values = np.array(decode_samples(selected_tick.values))
                        generated_metronome = MetronomeFile(frequency=int(request.POST['frequency']),
                                                            duration=int(request.POST['duration']),
                                                            bpm=int(request.POST['bpm']),
                                                            tick_values=metronome_tick_values,
                                                            stereo=request.POST.get('stereo', False))
                        write(metronome_url, generated_metronome.frequency, generated_metronome.samples)
                    a = AudioFile(metronome_url)
                    a.convert('mp3', True)
            else:
                context['errors'] = validate_form.errors
                return render(request, 'metronome/generate.html', context)
        metronome_url = metronome_url[:-3]+'mp3'
        metronome_name = metronome_name[:-3]+'mp3'
        context['generated_metronome_name'] = metronome_name
        context['generated_metronome_url'] = metronome_url

        if 'save_submit' in request.POST:
            validate_form = MetronomeSaveForm(data={'title': request.POST['title'],
                                                    'frequency': request.POST['frequency'],
                                                    'duration': request.POST['duration'],
                                                    'bpm': request.POST['bpm'],
                                                    'tick': Tick.objects.get(id=request.POST['tick']),
                                                    'stereo': True if request.POST.get('stereo') else False,
                                                    'user': request.user})
            if validate_form.is_valid():
                metronome = Metronome(title=request.POST['title'],
                                      user=request.user,
                                      frequency=request.POST['frequency'],
                                      duration=request.POST['duration'],
                                      bpm=request.POST['bpm'],
                                      tick=Tick.objects.get(id=request.POST['tick']),
                                      stereo=request.POST['stereo'])
                metronome.save()
            else:
                context['errors'] = validate_form.errors
                context['save_form'] = MetronomeSaveForm(initial={'frequency': request.POST['frequency'],
                                                                  'duration': request.POST['duration'],
                                                                  'bpm': request.POST['bpm'],
                                                                  'tick': request.POST['tick'],
                                                                  'user': request.user})
            # potentially to develop
            # redirect to metronomes/<metronome> or clear title input + message or hide save form
            # for now hide form
        else:
            if not request.user.is_anonymous:
                if request.POST.get('creation_submit', 'view') != 'view':
                    context['save_form'] = MetronomeSaveForm(initial={'frequency': request.POST['frequency'],
                                                                      'duration': request.POST['duration'],
                                                                      'bpm': request.POST['bpm'],
                                                                      'tick': request.POST['tick'],
                                                                      'user': request.user})

        return render(request, 'metronome/generate.html', context)


class Metronomes(View):
    def query(self, user):
        metronomes = []
        for metronome in Metronome.objects.filter(user=user):
            form = MetronomeSaveForm(initial={'frequency': metronome.frequency,
                                              'duration': metronome.duration,
                                              'bpm': metronome.bpm,
                                              'stereo': metronome.stereo,
                                              'tick': metronome.tick})
            metronomes.append({'metronome': metronome, 'form': form})
        return metronomes

    def get(self, request):
        context = {'metronomes': self.query(request.user)}
        return render(request, 'metronome/metronomes.html', context)

    def post(self, request):
        if 'confirm_id' in request.POST:
            delete_metronome = Metronome.objects.get(user=request.user, id=request.POST['delete_id'])
            delete_metronome.delete()
        context = {'metronomes': self.query(request.user),
                   'delete_id': int(request.POST.get('delete_id', 0))}
        return render(request, 'metronome/metronomes.html', context)
