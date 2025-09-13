from django import forms
from .models import Scholarship, CustomField, ApplicationStatus

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = Scholarship
        fields = [
            "name",
            "provider",
            "funding_type",
            "deadline",
            "flight_ticket_fee",
            "visa_application_fee",
            "work_permit_available",
            "description",
        ]
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class CustomFieldForm(forms.ModelForm):
    class Meta:
        model = CustomField
        fields = ["field_name", "field_value"]


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = ApplicationStatus
        fields = ["status", "notes"]
