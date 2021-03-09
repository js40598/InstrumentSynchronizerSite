from django.shortcuts import render
from django.views import View
from metronome.forms import MetronomeCreationForm

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
            'creation_form': self.form(),
        }
        return render(request, 'metronome/generate.html', context)


class Metronomes(View):
    def get(self, request):
        return render(request, 'metronome/generate.html')

    def post(self, request):
        return render(request, 'metronome/generate.html')
