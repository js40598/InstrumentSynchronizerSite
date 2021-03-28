from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.AudioFile import AudioFile
from InstrumentSynchronizerSite.InstrumentSynchronizer.instrsyn.Synchronizer import Synchronizer
from synchronizer.forms import ProjectCreationForm, RecordingAddForm, CutRecordingForm
from synchronizer.models import Project as ProjectModel
from synchronizer.models import Recording
import os
from InstrumentSynchronizerSite import settings


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
        context = {'projects': ProjectModel.objects.filter(user=request.user).order_by('-edition_date'),
                   'delete_id': int(request.POST.get('delete_id', 0))}
        return render(request, 'synchronizer/projects.html', context)


class CreateProject(View):
    form = ProjectCreationForm

    def get(self, request):
        context = {'creation_form': self.form()}
        return render(request, 'synchronizer/create_project.html', context)

    def post(self, request):
        creation_form = self.form(data={'user': request.user,
                                        'title': request.POST['title'],
                                        'bpm': request.POST['bpm'],
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
    def get(self, request, project_slug):
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        context = {'project': project}
        return render(request, 'synchronizer/project.html', context)

    def post(self, request, project_slug):
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        if 'confirm_id' in request.POST:
            recording = Recording.objects.get(id=request.POST['confirm_id'], project=project)
            recording.delete()

        context = {'project': project,
                   'delete_id': int(request.POST.get('delete_id', 0))}
        return render(request, 'synchronizer/project.html', context)


class AddRecording(View):
    form = RecordingAddForm

    def get(self, request, project_slug):
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        context = {'project': project,
                   'form': self.form()}
        return render(request, 'synchronizer/add_recording.html', context)

    def post(self, request, project_slug):
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        form = self.form(files=request.FILES, data={'instrument': request.POST['instrument'],
                                                    'identifier': request.POST['identifier'],
                                                    'pitch': request.POST['pitch'],
                                                    'author': request.POST['author'],
                                                    'project': project})
        if form.is_valid():
            recording = Recording(**form.cleaned_data)
            recording.save()
            recording_path = str(os.path.join(settings.RECORDINGS_ROOT, recording.file.name.split('/')[-1]))

            audio_file = AudioFile(recording_path)
            # if recording_path != audio_file.directory:
            #     os.remove(recording_path)
            recording.file = audio_file.directory
            recording.save()
            return redirect('cut_recording', project_slug, recording.slug)
        else:
            context = {'project': project,
                       'form': form,
                       'errors': form.errors}
            return render(request, 'synchronizer/add_recording.html', context)


class CutRecording(View):
    form = CutRecordingForm

    def get(self, request, project_slug, recording_slug):
        form = self.form(max_value=44100*20)
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        recording = Recording.objects.get(project=project, slug=recording_slug)
        recording_url = str(os.path.join(settings.RECORDINGS_ROOT, recording.file.name.split('/')[-1]))
        context = {'project': project,
                   'recording': recording,
                   'recording_url': recording_url,
                   'form': form}
        return render(request, 'synchronizer/cut_recording.html', context)

    def post(self, request, project_slug, recording_slug):
        project = ProjectModel.objects.get(slug=project_slug, user=request.user)
        recording = Recording.objects.get(project=project, slug=recording_slug)
        form = self.form(max_value=44100*20, value=request.POST['cut_index'], data=request.POST)
        if form.is_valid():
            file = AudioFile(str(os.path.join(settings.RECORDINGS_ROOT, recording.file.name.split('/')[-1])))
            file.cut_samples(int(request.POST['cut_index']))
            file.save_file()
            synchronized_file = Synchronizer(file.framerate,
                                             project.bpm,
                                             list(file.samplesleft),
                                             list(file.samplesright))
            file.samplesleft = synchronized_file.synchronized_samplesleft
            file.samplesright = synchronized_file.synchronized_samplesright
            file.save_file()
            recording.file = file.directory
            recording.save()
            return redirect('project', project_slug)
        else:
            recording_url = str(os.path.join(settings.RECORDINGS_ROOT, recording.file.name.split('/')[-1]))
            context = {'project': project,
                       'recording': recording,
                       'recording_url': recording_url,
                       'form': form}
            return render(request, 'synchronizer/cut_recording.html', context)


def view_recording(request, project_slug, recording_slug):
    project = ProjectModel.objects.get(slug=project_slug, user=request.user)
    recording = Recording.objects.get(project=project, slug=recording_slug)
    recording_url = os.path.join(settings.RECORDINGS_ROOT, recording.file.name)
    context = {'project': project,
               'recording': recording,
               'recording_url': recording_url}
    return render(request, 'synchronizer/view_recording.html', context)
