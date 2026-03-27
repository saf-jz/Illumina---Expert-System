from django import forms
from .models import Material, ServiceType


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["name", "complexity_score", "description", "active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "complexity_score": forms.NumberInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        existing_materials = Material.objects.filter(name__iexact=name)

        if self.instance.pk:
            existing_materials = existing_materials.exclude(pk=self.instance.pk)

        if existing_materials.exists():
            raise forms.ValidationError("A material with this name already exists.")

        return name



class ServiceTypeForm(forms.ModelForm):
    class Meta:
        model = ServiceType
        fields = ["name", "description", "base_complexity_score", "active"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "base_complexity_score": forms.NumberInput(attrs={"class": "form-control"}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        existing_services = ServiceType.objects.filter(name__iexact=name)

        if self.instance.pk:
            existing_services = existing_services.exclude(pk=self.instance.pk)

        if existing_services.exists():
            raise forms.ValidationError("A service type with this name already exists.")

        return name