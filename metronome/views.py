from django.shortcuts import render

# Create your views here.


def about(request):
    return render(request, 'metronome/about.html')


def howto(request):
    return render(request, 'metronome/howto.html')


def generate(request):
    return render(request, 'metronome/generate.html')


def metronomes(request):
    return render(request, 'metronome/metronomes.html')
