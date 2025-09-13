from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .models import Scholarship, CustomField
from .forms import ScholarshipForm


# 🔹 Dashboard View
@login_required
def dashboard(request):
    """
    Show user overview:
    - Total scholarships applied
    - Pending / Accepted / Rejected counts
    """
    scholarships = Scholarship.objects.filter(user=request.user)

    stats = {
        "applied": sum(1 for s in scholarships if s.current_status() == "applied"),
        "pending": sum(1 for s in scholarships if s.current_status() == "in_review"),
        "accepted": sum(1 for s in scholarships if s.current_status() == "accepted"),
        "rejected": sum(1 for s in scholarships if s.current_status() == "rejected"),
    }


    return render(request, "scholarship_tracker_app/dashboard.html", {"stats": stats, "scholarships": scholarships})


# 🔹 List Scholarships
@login_required
def scholarship_list(request):
    """
    Display all scholarships for the logged-in user in a table.
    Supports simple search and filter.
    """
    scholarships = Scholarship.objects.filter(user=request.user)

    # search bar
    query = request.GET.get("q")
    if query:
        scholarships = scholarships.filter(name__icontains=query)

    # status filter
    status = request.GET.get("status")
    if status and status != "All":
        scholarships = scholarships.filter(status=status)

    return render(request, "scholarship_tracker_app/scholarship_list.html", {"scholarships": scholarships})


# 🔹 Scholarship Detail
@login_required
def scholarship_detail(request, pk):
    """
    Show details for a single scholarship
    - Overview (fields)
    - Custom fields
    - AI summary placeholder (for Phase 2)
    """
    scholarship = get_object_or_404(Scholarship, pk=pk, user=request.user)
    custom_fields = CustomField.objects.filter(scholarship=scholarship)

    return render(
        request,
        "scholarship_tracker_app/scholarship_detail.html",
        {"scholarship": scholarship, "custom_fields": custom_fields},
    )


# 🔹 Add Scholarship
@login_required
def add_scholarship(request):
    """
    Form to add new scholarship with dynamic custom fields.
    """
    if request.method == "POST":
        form = ScholarshipForm(request.POST)
        if form.is_valid():
            scholarship = form.save(commit=False)
            scholarship.user = request.user
            scholarship.save()

            # Handle dynamic custom fields
            keys = request.POST.getlist("custom_key[]")
            values = request.POST.getlist("custom_value[]")
            for k, v in zip(keys, values):
                if k and v:
                    CustomField.objects.create(scholarship=scholarship,  field_name=k, field_value=v)

            messages.success(request, "Scholarship added successfully.")
            return redirect("scholarship_list")
    else:
        form = ScholarshipForm()

    return render(request, "scholarship_tracker_app/scholarship_form.html", {"form": form})


# 🔹 Edit Scholarship
@login_required
def edit_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk, user=request.user)

    if request.method == "POST":
        form = ScholarshipForm(request.POST, instance=scholarship)
        if form.is_valid():
            form.save()

            # Reset custom fields
            CustomField.objects.filter(scholarship=scholarship).delete()
            keys = request.POST.getlist("custom_key[]")
            values = request.POST.getlist("custom_value[]")
            for k, v in zip(keys, values):
                if k and v:
                    CustomField.objects.create(scholarship=scholarship, key=k, value=v)

            messages.success(request, "Scholarship updated successfully.")
            return redirect("scholarship_detail", pk=pk)
    else:
        form = ScholarshipForm(instance=scholarship)

    custom_fields = CustomField.objects.filter(scholarship=scholarship)
    return render(
        request, "scholarship_tracker_app/scholarship_form.html", {"form": form, "scholarship": scholarship, "custom_fields": custom_fields}
    )


# 🔹 Delete Scholarship
@login_required
def delete_scholarship(request, pk):
    scholarship = get_object_or_404(Scholarship, pk=pk, user=request.user)

    if request.method == "POST":
        scholarship.delete()
        messages.success(request, "Scholarship deleted successfully.")
        return redirect("scholarship_list")

    return render(request, "scholarship_tracker_app/confirm_delete.html", {"scholarship": scholarship})


# 🔹 Settings Page (for Phase 4 WhatsApp etc.)
@login_required
def settings_view(request):
    """
    Simple settings page:
    - WhatsApp forwarding toggle
    - WhatsApp number input
    """
    if request.method == "POST":
        whatsapp_forward = request.POST.get("whatsapp_forward") == "on"
        whatsapp_number = request.POST.get("whatsapp_number")

        # Save in user profile (assume extended UserProfile model)
        profile = request.user.profile
        profile.whatsapp_forward = whatsapp_forward
        profile.whatsapp_number = whatsapp_number
        profile.save()

        messages.success(request, "Settings updated.")
        return redirect("settings")

    return render(request, "settings.html")
