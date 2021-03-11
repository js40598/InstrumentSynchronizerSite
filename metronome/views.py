from django.shortcuts import render
from django.views import View
from metronome.forms import MetronomeCreationForm, MetronomeSaveForm
from metronome.models import Metronome, Tick

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
