from django.urls import path
from . import views

app_name = "student"
urlpatterns = [
    path("", views.StudentDetailView.as_view(), name="index"),
    path("course/", views.CourseIndexView.as_view(), name="course-index"),
    path(
        "course_purchase/create/",
        views.CoursePurchaseCreateView.as_view(),
        name="course_purchase-create",
    ),
    path(
        "course_purchase/<int:pk>/",
        views.CoursePurchaseDetailView.as_view(),
        name="course_purchase-detail",
    ),
    path(
        "course_attending/create/",
        views.CourseAttendingCreateView.as_view(),
        name="course_attending-create",
    ),
    path(
        "course_attending/<int:pk>/update/",
        views.CourseAttendingUpdateView.as_view(),
        name="course_attending-update",
    ),
    path(
        "course_attending/<int:pk>/",
        views.CourseAttendingDetailView.as_view(),
        name="course_attending-detail",
    ),
    path(
        "section_attending/create/",
        views.SectionAttendingCreateView.as_view(),
        name="section_attending-create",
    ),
    path(
        "section_attending/<int:pk>/",
        views.SectionAttendingDetailView.as_view(),
        name="section_attending-detail",
    ),
    path(
        "content_attending/create/",
        views.ContentAttendingCreateView.as_view(),
        name="content_attending-create",
    ),
    path(
        "content_attending/<int:pk>/",
        views.ContentAttendingDetailView.as_view(),
        name="content_attending-detail",
    ),
    path(
        "exam_result/create/",
        views.ExamResultCreateView.as_view(),
        name="exam_result-create",
    ),
    path(
        "exam_result/<int:pk>/",
        views.ExamResultDetailView.as_view(),
        name="exam_result-detail",
    ),
    path("answer/", views.answer, name="answer"),
    path(
        "question/create/", views.QuestionCreateView.as_view(), name="question-create"
    ),
    path(
        "question/<int:pk>/update/",
        views.QuestionUpdateView.as_view(),
        name="question-update",
    ),
    path(
        "question/<int:pk>/delete/",
        views.QuestionDeleteView.as_view(),
        name="question-delete",
    ),
    path(
        "question/<int:pk>/", views.QuestionDetailView.as_view(), name="question-detail"
    ),
]