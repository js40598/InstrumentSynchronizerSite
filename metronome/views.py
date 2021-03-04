from django.shortcuts import render

# Create your views here.
from django.views import View


def about(request):
    return render(request, 'metronome/about.html')


def howto(request):
    return render(request, 'metronome/howto.html')


class Generate(View):
    def get(self, request):
        return render(request, 'metronome/generate.html')

    def post(self, request):
        return render(request, 'metronome/generate.html')


class Metronomes(View):
    def get(self, request):
        return render(request, 'metronome/generate.html')

    def post(self, request):
        return render(request, 'metronome/generate.html')
