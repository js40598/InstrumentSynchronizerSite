from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import RegisterForm


class Login(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        return render(request, 'accounts/login.html')


class Register(View):
    register_form = RegisterForm

    def get(self, request):
        form = self.register_form()
        context = {
            'form': form,
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        return render(request, 'accounts/register.html')


@login_required
def logoutuser(request):
    logout(request)
    return redirect('landing')
