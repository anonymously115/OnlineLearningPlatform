from django.urls import path
from . import views

app_name = "teacher"
urlpatterns = [
    path("", views.TeacherDetailView.as_view(), name="index"),
    path("course/create/", views.CourseCreateView.as_view(), name="course-create"),
    path(
        "course/<int:pk>/update/",
        views.CourseUpdateView.as_view(),
        name="course-update",
    ),
    path(
        "course/<int:pk>/delete/",
        views.CourseDeleteView.as_view(),
        name="course-delete",
    ),
    path("course/<int:pk>/", views.CourseDetailView.as_view(), name="course-detail"),
    path("section/create/", views.SectionCreateView.as_view(), name="section-create"),
    path(
        "section/<int:pk>/update/",
        views.SectionUpdateView.as_view(),
        name="section-update",
    ),
    path(
        "section/<int:pk>/delete/",
        views.SectionDeleteView.as_view(),
        name="section-delete",
    ),
    path("section/<int:pk>/", views.SectionDetailView.as_view(), name="section-detail"),
    path(
        "lecture_video/create/",
        views.LectureVideoCreateView.as_view(),
        name="lecture_video-create",
    ),
    path(
        "lecture_video/<int:pk>/update/",
        views.LectureVideoUpdateView.as_view(),
        name="lecture_video-update",
    ),
    path(
        "lecture_video/<int:pk>/delete/",
        views.LectureVideoDeleteView.as_view(),
        name="lecture_video-delete",
    ),
    path(
        "lecture_video/<int:pk>/",
        views.LectureVideoDetailView.as_view(),
        name="lecture_video-detail",
    ),
    path(
        "examination/create/",
        views.ExaminationCreateView.as_view(),
        name="examination-create",
    ),
    path(
        "examination/<int:pk>/update/",
        views.ExaminationUpdateView.as_view(),
        name="examination-update",
    ),
    path(
        "examination/<int:pk>/delete/",
        views.ExaminationDeleteView.as_view(),
        name="examination-delete",
    ),
    path(
        "examination/<int:pk>/",
        views.ExaminationDetailView.as_view(),
        name="examination-detail",
    ),
    path(
        "exam_question/create/",
        views.ExamQuestionCreateView.as_view(),
        name="exam_question-create",
    ),
    path(
        "exam_question/<int:pk>/update/",
        views.ExamQuestionUpdateView.as_view(),
        name="exam_question-update",
    ),
    path(
        "exam_question/<int:pk>/delete/",
        views.ExamQuestionDeleteView.as_view(),
        name="exam_question-delete",
    ),
    path(
        "exam_question/<int:pk>/",
        views.ExamQuestionDetailView.as_view(),
        name="exam_question-detail",
    ),
    path(
        "exam_question_choice/create/",
        views.ExamQuestionChoiceCreateView.as_view(),
        name="exam_question_choice-create",
    ),
    path(
        "exam_question_choice/<int:pk>/update/",
        views.ExamQuestionChoiceUpdateView.as_view(),
        name="exam_question_choice-update",
    ),
    path(
        "exam_question_choice/<int:pk>/delete/",
        views.ExamQuestionChoiceDeleteView.as_view(),
        name="exam_question_choice-delete",
    ),
    path(
        "exam_question_choice/<int:pk>/",
        views.ExamQuestionChoiceDetailView.as_view(),
        name="exam_question_choice-detail",
    ),
    path("coupon/create/", views.CouponCreateView.as_view(), name="coupon-create"),
    path(
        "coupon/<int:pk>/update/",
        views.CouponUpdateView.as_view(),
        name="coupon-update",
    ),
    path(
        "coupon/<int:pk>/delete/",
        views.CouponDeleteView.as_view(),
        name="coupon-delete",
    ),
    path("coupon/<int:pk>/", views.CouponDetailView.as_view(), name="coupon-detail"),
    path("comment/create/", views.CommentCreateView.as_view(), name="comment-create"),
]