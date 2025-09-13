from django.db import models
from django.contrib.auth.models import User

class Scholarship(models.Model):
    FUNDING_CHOICES = [
        ("full", "Full Funding"),
        ("partial", "Partial Funding"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scholarships")
    name = models.CharField(max_length=255)
    provider = models.CharField(max_length=255, blank=True, null=True)
    funding_type = models.CharField(max_length=20, choices=FUNDING_CHOICES)
    deadline = models.DateField(blank=True, null=True)
    flight_ticket_fee = models.BooleanField(default=False)
    visa_application_fee = models.BooleanField(default=False)
    work_permit_available = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.funding_type})"
    
    def current_status(self):
        latest = self.statuses.order_by("-updated_at").first()
        return latest.status if latest else "applied"
    
    def latest_status_date(self):
        latest = self.statuses.order_by("-updated_at").first()
        return latest.updated_at if latest else None

class CustomField(models.Model):
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name="custom_fields")
    field_name = models.CharField(max_length=255)
    field_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.field_name}: {self.field_value}"


class ApplicationStatus(models.Model):
    STATUS_CHOICES = [
        ("applied", "Applied"),
        ("in_review", "In Review"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name="statuses")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="applied")
    notes = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.scholarship.name} - {self.status}"
