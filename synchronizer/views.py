from django.shortcuts import render, redirect

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
        projects = ProjectModel.objects.filter(user=request.user).order_by('-edition_date')
        context = {'projects': projects}
        return render(request, 'synchronizer/projects.html', context)

    def post(self, request):
        if 'confirm_id' in request.POST:
            project = ProjectModel.objects.get(id=request.POST['confirm_id'], user=request.user)
            project.delete()
        context = {'projects': ProjectModel.objects.filter(user=request.user).order_by('edition_date'),
                   'delete_id': int(request.POST.get('delete_id', 0))}
        return render(request, 'synchronizer/projects.html', context)


class Create(View):
    form = ProjectCreationForm

    def get(self, request):
        context = {'creation_form': self.form()}
        return render(request, 'synchronizer/create_project.html', context)

    def post(self, request):
        creation_form = self.form(data={'user': request.user,
                                        'title': request.POST['title'],
                                        'description': request.POST['description'],
                                        })
        if creation_form.is_valid():
            project = ProjectModel(**creation_form.cleaned_data)
            project.save()
            return redirect('projects')
        context = {'creation_form': creation_form,
                   'errors': creation_form.errors}
        return render(request, 'synchronizer/create_project.html', context)


class Project(View):
    def get(self, request, project_name):
        return render(request, 'synchronizer/project.html')

    def post(self, request, project_name):
        return render(request, 'synchronizer/project.html')
