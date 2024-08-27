"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
import os
import json
from django.conf import settings

def index(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'mock-data', 'configs.json') # Acá debería leer datos de la db
    with open(json_file_path, 'r', encoding='utf-8') as file:
        on_load_data = json.load(file)

    return render(request, 'index.html', on_load_data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home', ),
    path('usermenu/', include('usermenu.urls')),
]
