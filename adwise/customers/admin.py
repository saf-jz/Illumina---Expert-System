from django.contrib import admin
from .models import Customer, Enquiry


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone",
        "email",
        "customer_category",
        "account_manager",
        "created_by",
        "created_at",
    )
    list_filter = ("customer_category", "created_at")
    search_fields = ("name", "phone", "email")
    ordering = ("name",)



@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = (
        "customer_name",
        "phone",
        "email",
        "assigned_to",
        "status",
        "created_at",
    )
    list_filter = ("status", "assigned_to", "created_at")
    search_fields = ("customer_name", "phone", "email", "message")
    ordering = ("-created_at",)
