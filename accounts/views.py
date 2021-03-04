from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.


def login(request):
    return render(request, 'accounts/login.html')


def register(request):
    return render(request, 'accounts/register.html')


@login_required
def logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')
    else:
        return redirect('home')
