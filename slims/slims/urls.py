"""
URL configuration for slims project.

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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from slims.api.views import router

urlpatterns = [
    path('admin/', admin.site.urls),
    path("runs/", views.runs, name="runs"),
    path("runs/<int:pk>/", views.run, name="run"),
    path("runs/<int:pk>/edit/", views.edit_run, name="edit_run"),
    path("users/", views.users, name="users"),
    path("users/<int:pk>/", views.profile, name="profile"),
    path("profile/", views.profile, name="profile"),
    path("groups/", views.groups, name="groups"),
    path("groups/<int:pk>/", views.group, name="group"),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
