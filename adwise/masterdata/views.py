from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views import View

from accounts.models import CustomUser
from .models import Material, ServiceType
from .forms import MaterialForm, ServiceTypeForm


@method_decorator(login_required, name="dispatch")
class MaterialListView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            messages.error(request, "Unauthorized access.")
            return redirect("accounts:role_redirect")

        materials = Material.objects.all()

        return render(request, "masterdata/material_list.html", {
            "materials": materials
        })



@method_decorator(login_required, name="dispatch")
class MaterialCreateView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        form = MaterialForm()
        return render(request, "masterdata/material_form.html", {"form": form})

    def post(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        form = MaterialForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Material created successfully.")
            return redirect("masterdata:material_list")

        return render(request, "masterdata/material_form.html", {"form": form})



@method_decorator(login_required, name="dispatch")
class MaterialUpdateView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        material = get_object_or_404(Material, pk=pk)
        form = MaterialForm(instance=material)

        return render(request, "masterdata/material_form.html", {
            "form": form,
            "object": material
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        material = get_object_or_404(Material, pk=pk)
        form = MaterialForm(request.POST, instance=material)

        if form.is_valid():
            form.save()
            messages.success(request, "Material updated successfully.")
            return redirect("masterdata:material_list")

        return render(request, "masterdata/material_form.html", {
            "form": form,
            "object": material
        })



@method_decorator(login_required, name="dispatch")
class ServiceTypeListView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        services = ServiceType.objects.all()

        return render(request, "masterdata/service_type_list.html", {
            "service_types": services
        })



@method_decorator(login_required, name="dispatch")
class ServiceTypeCreateView(View):
    def get(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        form = ServiceTypeForm()
        return render(request, "masterdata/service_type_form.html", {"form": form})

    def post(self, request):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        form = ServiceTypeForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Service type created successfully.")
            return redirect("masterdata:service_type_list")

        return render(request, "masterdata/service_type_form.html", {"form": form})



@method_decorator(login_required, name="dispatch")
class ServiceTypeUpdateView(View):
    def get(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        service = get_object_or_404(ServiceType, pk=pk)
        form = ServiceTypeForm(instance=service)

        return render(request, "masterdata/service_type_form.html", {
            "form": form,
            "object": service
        })

    def post(self, request, pk):
        if request.user.role != CustomUser.ADMIN:
            return redirect("accounts:role_redirect")

        service = get_object_or_404(ServiceType, pk=pk)
        form = ServiceTypeForm(request.POST, instance=service)

        if form.is_valid():
            form.save()
            messages.success(request, "Service type updated successfully.")
            return redirect("masterdata:service_type_list")

        return render(request, "masterdata/service_type_form.html", {
            "form": form,
            "object": service
        })