from django.shortcuts import render

# Create your views here.
from django.views import View
from synchronizer.forms import ProjectCreationForm
from synchronizer.models import Project as ProjectModel
from synchronizer.models import Recording


def about(request):
    return render(request, 'synchronizer/about.html')


def howto(request):
    return render(request, 'synchronizer/howto.html')


class Projects(View):
    def get(self, request):
        creation_form = ProjectCreationForm()
        context = {'creation_form': creation_form}
        return render(request, 'synchronizer/projects.html', context)

    def post(self, request):
        creation_form = ProjectCreationForm(data={'user': request.user,
                                                  'title': request.POST['title'],
                                                  'description': request.POST['description'],
                                                  })
        if creation_form.is_valid():
            project = ProjectModel(**creation_form.cleaned_data)
            project.save()
        context = {'creation_form': creation_form,
                   'errors': creation_form.errors}
        return render(request, 'synchronizer/projects.html', context)


class Project(View):
    def get(self, request, project_name):
        return render(request, 'synchronizer/project.html')

    def post(self, request, project_name):
        return render(request, 'synchronizer/project.html')
