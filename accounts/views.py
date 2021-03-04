from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from django.views import View


class Login(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        return render(request, 'accounts/login.html')


class Register(View):
    def get(self, request):
        return render(request, 'accounts/register.html')

    def post(self, request):
        return render(request, 'accounts/register.html')


@login_required
def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
