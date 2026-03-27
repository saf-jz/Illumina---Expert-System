from django.db import models
from django.conf import settings


class Quote(models.Model):
    DRAFT = "DRAFT"
    SUBMITTED = "SUBMITTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    STATUS_CHOICES = [
        (DRAFT, "Draft"),
        (SUBMITTED, "Submitted"),
        (UNDER_REVIEW, "Under Review"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    URGENCY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    SMALL = "SMALL"
    MEDIUM_SIZE = "MEDIUM"
    LARGE = "LARGE"


    SIZE_CHOICES = [
        (SMALL, "Small"),
        (MEDIUM_SIZE, "Medium"),
        (LARGE, "Large"),
    ]

    REGULAR = "REGULAR"
    CORPORATE = "CORPORATE"
    VIP = "VIP"

    CUSTOMER_CATEGORY_CHOICES = [
        (REGULAR, "Regular"),
        (CORPORATE, "Corporate"),
        (VIP, "VIP"),
    ]

    customer = models.ForeignKey(
        "customers.Customer",
        on_delete=models.CASCADE,
        related_name="quotes"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotes_created"
    )
    service_type = models.ForeignKey(
        "masterdata.ServiceType",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotes"
    )
    material = models.ForeignKey(
        "masterdata.Material",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotes"
    )
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(
        max_length=20,
        choices=SIZE_CHOICES,
        null=True,
        blank=True
    )
    urgency = models.CharField(
        max_length=20,
        choices=URGENCY_CHOICES,
        default=LOW
    )
    installation_required = models.BooleanField(default=False)
    customer_category = models.CharField(
        max_length=20,
        choices=CUSTOMER_CATEGORY_CHOICES
    )
    job_description = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Quote #{self.id} - {self.customer}"


class SystemRecommendation(models.Model):
    SYSTEM_RECOMMENDATION = "SYSTEM"
    PRELIMINARY_RECOMMENDATION = "PRELIMINARY"

    RECOMMENDATION_TYPE_CHOICES = [
        (SYSTEM_RECOMMENDATION, "System Recommendation"),
        (PRELIMINARY_RECOMMENDATION, "Preliminary Recommendation"),
    ]

    quote = models.OneToOneField(
        Quote,
        on_delete=models.CASCADE,
        related_name="system_recommendation"
    )
    system_price_tier = models.CharField(max_length=50)
    system_margin_range = models.CharField(max_length=50)
    system_approval_recommendation = models.CharField(max_length=100)
    system_explanation = models.TextField()
    recommendation_type = models.CharField(
        max_length=20,
        choices=RECOMMENDATION_TYPE_CHOICES,
        default=SYSTEM_RECOMMENDATION
    )
    total_score = models.PositiveIntegerField()
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-generated_at"]

    def __str__(self):
        return f"Recommendation for Quote #{self.quote.id}"


class AdminDecision(models.Model):
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

    DECISION_CHOICES = [
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
    ]

    quote = models.OneToOneField(
        Quote,
        on_delete=models.CASCADE,
        related_name="admin_decision"
    )
    admin_decision = models.CharField(
        max_length=20,
        choices=DECISION_CHOICES
    )
    admin_notes = models.TextField(blank=True)
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reviewed_quotes"
    )
    reviewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-reviewed_at"]

    def __str__(self):
        return f"Admin Decision for Quote #{self.quote.id}"