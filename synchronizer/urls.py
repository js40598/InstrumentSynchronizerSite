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
from django.urls import path
from synchronizer import views

urlpatterns = [
    path('about/', views.about, name='synchronizerabout'),
    path('howto/', views.howto, name='synchronizerhowto'),
    path('projects/', views.Projects.as_view(), name='projects'),
    path('create/', views.Create.as_view(), name='create_project'),
    path('projects/<project_title>', views.Project.as_view(), name='project'),
]
