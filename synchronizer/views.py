from django.shortcuts import render

# Create your views here.


def about(request):
    return render(request, 'synchronizer/about.html')


def howto(request):
    return render(request, 'synchronizer/howto.html')


def synchronize(request):
    return render(request, 'synchronizer/synchronize.html')


def projects(request):
    return render(request, 'synchronizer/projects.html')
