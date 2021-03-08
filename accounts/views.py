from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.views import View

from InstrumentSynchronizerSite.validators import PasswordsMatchValidator
from accounts.forms import RegisterForm


class Login(View):
    login_form = AuthenticationForm

    def get(self, request):
        return render(request, 'accounts/login.html', {'form': self.login_form()})

    def post(self, request):
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'accounts/login.html', {'form': self.login_form, 'error': 'login failed'})
        else:
            login(request, user)
            return redirect('landing')


class Register(View):
    register_form = RegisterForm

    def get(self, request):
        form = self.register_form()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        form = self.register_form()
        user = User(
            username=request.POST['username'],
            email=request.POST['email'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
        )
        with transaction.atomic():
            # validators (to develop)
            validator = PasswordsMatchValidator(request.POST['password1'], request.POST['password2'])
            if validator.is_valid:
                # save user model in database
                user = User(
                    username=request.POST['username'],
                    password=request.POST['password1'],
                    email=request.POST['email'],
                    first_name=request.POST['first_name'],
                    last_name=request.POST['last_name'],
                )
                user.save()
                login(request, user)
                return redirect('landing')
            else:
                return render(request, 'accounts/register.html', {'form': form,
                                                                  'values': user,
                                                                  'error': validator.message})


@login_required
def logoutuser(request):
    logout(request)
    return redirect('landing')
