from django.shortcuts import render

# Create your views here.
from django.views import View


def about(request):
    return render(request, 'synchronizer/about.html')


def howto(request):
    return render(request, 'synchronizer/howto.html')


class Projects(View):
    def get(self, request):
        return render(request, 'synchronizer/projects.html')

    def post(self, request):
        return render(request, 'synchronizer/projects.html')


class Project(View):
    def get(self, request):
        return render(request, 'synchronizer/synchronize.html')

    def post(self, request):
        return render(request, 'synchronizer/synchronize.html')
