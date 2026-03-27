from django.contrib import admin
from .models import Quote, SystemRecommendation, AdminDecision


@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "customer",
        "created_by",
        "service_type",
        "material",
        "quantity",
        "status",
        "created_at",
    )
    list_filter = ("status", "urgency", "installation_required", "created_at")
    search_fields = ("customer__name", "salesperson__username")
    ordering = ("-created_at",)



@admin.register(SystemRecommendation)
class SystemRecommendationAdmin(admin.ModelAdmin):
    list_display = (
        "quote",
        "system_price_tier",
        "system_margin_range",
        "system_approval_recommendation",
        "recommendation_type",
        "total_score",
        "generated_at",
    )
    list_filter = ("recommendation_type", "generated_at")
    search_fields = ("quote__customer__name",)
    ordering = ("-generated_at",)



@admin.register(AdminDecision)
class AdminDecisionAdmin(admin.ModelAdmin):
    list_display = (
        "quote",
        "admin_decision",
        "reviewed_by",
        "reviewed_at",
    )
    list_filter = ("admin_decision", "reviewed_at")
    search_fields = ("quote__customer__name", "reviewed_by__username")
    ordering = ("-reviewed_at",)
