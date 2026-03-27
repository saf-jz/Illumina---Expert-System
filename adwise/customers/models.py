from django.db import models
from django.conf import settings


class Customer(models.Model):
    REGULAR = "REGULAR"
    CORPORATE = "CORPORATE"
    VIP = "VIP"

    CATEGORY_CHOICES = [
        (REGULAR, "Regular"),
        (CORPORATE, "Corporate"),
        (VIP, "VIP"),
    ]

    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    company_name = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    customer_category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default=REGULAR
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers_created"
    )
    account_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="customers_managed"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        if self.company_name:
            return f"{self.company_name} ({self.name})"
        return self.name


class Enquiry(models.Model):
    NEW = "NEW"
    ASSIGNED = "ASSIGNED"
    CLOSED = "CLOSED"

    STATUS_CHOICES = [
        (NEW, "New"),
        (ASSIGNED, "Assigned"),
        (CLOSED, "Closed"),
    ]

    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    message = models.TextField()

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="enquiries"
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_enquiries"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=NEW
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Enquiries"

    def __str__(self):
        return f"{self.customer_name} - {self.status}"