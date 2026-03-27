from django.contrib import admin
from .models import Material, ServiceType


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "complexity_score", "active")
    list_filter = ("active",)
    search_fields = ("name",)
    ordering = ("name",)



@admin.register(ServiceType)
class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "base_complexity_score", "active")
    list_filter = ("active",)
    search_fields = ("name",)
    ordering = ("name",)
