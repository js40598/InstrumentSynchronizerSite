"""InstrumentSynchronizerSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib.auth.decorators import login_required
from django.urls import path
from metronome import views

urlpatterns = [
    path('about/', views.about, name='metronomeabout'),
    path('howto/', views.howto, name='metronomehowto'),
    path('generate/', views.Generate.as_view(), name='generate'),
    path('metronomes/', login_required(views.Metronomes.as_view()), name='metronomes'),
    path('download_metronome/<metronome_name>', views.download_metronome, name='download_metronome'),
]
