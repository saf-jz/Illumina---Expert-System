from django.db import models


class Material(models.Model):
    name = models.CharField(max_length=100, unique=True)
    complexity_score = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name



class ServiceType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    base_complexity_score = models.PositiveIntegerField()
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Service Type"
        verbose_name_plural = "Service Types"

    def __str__(self):
        return self.name
