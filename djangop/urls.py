"""
URL configuration for djangop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', name='home', view=home),
    path('login/', name='login', view=login),
    path('video/', name='video', view=video),
    path('register/', name='register', view=register),
    path('authenticate/', name='authenticate', view=authenticate),
    path('logout/', name='logout', view=logout),
    path('upload/', name='upload', view=upload),
    path('subscriptions/', name='subscriptions', view=sub),
    path('liked/', name='like', view=like),
    path('user/', name='myvideos', view=myvideos),
    path('delete/', name='delete', view=delete)
]

from django.conf.urls.static import static
from django.conf import settings

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)