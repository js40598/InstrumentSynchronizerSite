from django.shortcuts import render

# Create your views here.


def landing(request):
    return render(request, 'pages/landing.html')


def about(request):
    return render(request, 'pages/about.html')


def contact(request):
    return render(request, 'pages/contact.html')
