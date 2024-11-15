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
from django.conf import settings
from usermenu.models import OrgConfig
from usermenu.context_processors import selected_category
from django.conf.urls.static import static
# No debería estar llamando al index desde acá, hay que moverlo al usermenu. Acá una landing simple y fue
def index(request):
    configs = (OrgConfig.objects.get(id_organization = 1))
    category = selected_category(request).get("get_category")()
    category = category["selected_category"]
    return render(request, 'index.html', {'configs': configs, 'selected_category': category})

urlpatterns = [
    path('', index, name='home', ),
    path('usermenu/', include('usermenu.urls')),
]