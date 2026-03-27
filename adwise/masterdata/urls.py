"""
URL configuration for adwise project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from masterdata import views

app_name = "masterdata"

urlpatterns = [
    # MATERIAL
    path("materials/", views.MaterialListView.as_view(), name="material_list"),
    path("materials/create/", views.MaterialCreateView.as_view(), name="material_create"),
    path("materials/<int:pk>/edit/", views.MaterialUpdateView.as_view(), name="material_update"),

    # SERVICE TYPE
    path("service-types/", views.ServiceTypeListView.as_view(), name="service_type_list"),
    path("service-types/create/", views.ServiceTypeCreateView.as_view(), name="service_type_create"),
    path("service-types/<int:pk>/edit/", views.ServiceTypeUpdateView.as_view(), name="service_type_update"),
]
