
from django.urls import path
from . import views

urlpatterns = [
    # 🔹 Dashboard
    path("", views.dashboard, name="dashboard"),

    # 🔹 Scholarship CRUD
    path("scholarships/", views.scholarship_list, name="scholarship_list"),
    path("scholarships/add/", views.add_scholarship, name="add_scholarship"),
    path("scholarships/<int:pk>/", views.scholarship_detail, name="scholarship_detail"),
    path("scholarships/<int:pk>/edit/", views.edit_scholarship, name="edit_scholarship"),
    path("scholarships/<int:pk>/delete/", views.delete_scholarship, name="delete_scholarship"),

    # 🔹 Settings
    path("settings/", views.settings_view, name="settings"),
]
