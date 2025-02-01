from django.urls import path
from . import views

app_name = "online_learning_platform"
urlpatterns = [
    path("", views.AccountDetailView.as_view(), name="index"),
    path("teacher/create/", views.TeacherCreateView.as_view(), name="teacher-create"),
    path("teacher/update/", views.TeacherUpdateView.as_view(), name="teacher-update"),
    path("teacher/delete/", views.TeacherDeleteView.as_view(), name="teacher-delete"),
    path("student/create/", views.StudentCreateView.as_view(), name="student-create"),
    path("student/update/", views.StudentUpdateView.as_view(), name="student-update"),
    path("student/delete/", views.StudentDeleteView.as_view(), name="student-delete"),
]
