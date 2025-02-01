from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Max
from django.db.models.base import Model
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from online_learning_platform.models import Account, Teacher
from .models import (
    Content,
    Coupon,
    Course,
    ExamQuestion,
    ExamQuestionChoice,
    Examination,
    LectureVideo,
    Section,
)
from student.models import Question, Comment


# Create your views here.
class TeacherDetailView(LoginRequiredMixin, generic.DetailView):
    model = Teacher

    def get_object(self) -> Model:
        return self.model.objects.get(
            account_ptr=Account.objects.get(user_ptr=self.request.user)
        )

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        teacher: Teacher = context_data["object"]
        context_data["courses"] = Course.objects.filter(teacher=teacher)
        return context_data


class CourseCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Course
    fields = ["course_name", "standard_price"]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        course: Course = form.instance
        course.teacher = Teacher.objects.get(user_ptr=self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("teacher:index")


class CourseUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Course
    fields = ["course_name", "standard_price"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course: Course = self.get_object()
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:course-detail", kwargs={"pk": self.get_object().pk}
        )


class CourseDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Course
    success_url = reverse_lazy("teacher:index")

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course: Course = self.get_object()
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)


class CourseDetailView(LoginRequiredMixin, generic.DetailView):
    model = Course

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course: Course = self.get_object()
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        course: Course = context_data["object"]
        context_data["sections"] = Section.objects.filter(course=course)
        context_data["coupons"] = Coupon.objects.filter(course=course)
        return context_data


class SectionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Section
    fields = ["section_name"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course: Course = get_object_or_404(
            Course, id=getattr(request, request.method)["course_id"]
        )
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["course_id"] = getattr(self.request, self.request.method)[
            "course_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        section: Section = form.instance
        section.course = Course.objects.get(
            id=getattr(self.request, self.request.method)["course_id"]
        )
        query_set = Section.objects.filter(course=section.course)
        section.section_no = 1
        if query_set:
            section.section_no += query_set.aggregate(Max("section_no"))[
                "section_no__max"
            ]
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:course-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["course_id"]},
        )


class SectionUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Section
    fields = ["section_name"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section: Section = self.get_object()
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:section-detail", kwargs={"pk": self.get_object().pk}
        )


class SectionDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Section

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section: Section = self.get_object()
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:course-detail", kwargs={"pk": self.get_object().course.pk}
        )


class SectionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Section

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section: Section = self.get_object()
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        section: Section = context_data["object"]
        context_data["videos"] = LectureVideo.objects.filter(section=section)
        query_set_exam = Examination.objects.filter(section=section)
        context_data["exam"] = query_set_exam.get() if query_set_exam else None
        return context_data


class LectureVideoCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = LectureVideo
    fields = ["content_name", "lecture_time"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section: Section = get_object_or_404(
            Section, id=getattr(request, request.method)["section_id"]
        )
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["section_id"] = getattr(self.request, self.request.method)[
            "section_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        video: LectureVideo = form.instance
        video.section = Section.objects.get(
            id=getattr(self.request, self.request.method)["section_id"]
        )
        query_set = LectureVideo.objects.filter(section=video.section)
        video.content_no = 1
        if query_set:
            video.content_no += query_set.aggregate(Max("content_no"))[
                "content_no__max"
            ]
        video.content_flag = False
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:section-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["section_id"]},
        )


class LectureVideoUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = LectureVideo
    fields = ["content_name", "lecture_time"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        video: LectureVideo = self.get_object()
        section: Section = video.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:lecture_video-detail", kwargs={"pk": self.get_object().pk}
        )


class LectureVideoDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = LectureVideo

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        video: LectureVideo = self.get_object()
        section: Section = video.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:section-detail", kwargs={"pk": self.get_object().section.pk}
        )


class LectureVideoDetailView(LoginRequiredMixin, generic.DetailView):
    model = LectureVideo

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        video: LectureVideo = self.get_object()
        section: Section = video.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        video: LectureVideo = context_data["object"]
        context_data["questions"] = Question.objects.prefetch_related("comment_set").filter(
            content_id=video.content_ptr_id
        )
        return context_data


class ExaminationCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Examination
    fields = ["content_name", "answer_limit_time"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        section: Section = get_object_or_404(
            Section, id=getattr(request, request.method)["section_id"]
        )
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["section_id"] = getattr(self.request, self.request.method)[
            "section_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        exam: Examination = form.instance
        exam.section = Section.objects.get(
            id=getattr(self.request, self.request.method)["section_id"]
        )
        exam.content_no = 0
        exam.content_flag = True
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:section-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["section_id"]},
        )


class ExaminationUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Examination
    fields = ["content_name", "answer_limit_time"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        exam: Examination = self.get_object()
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:examination-detail", kwargs={"pk": self.get_object().pk}
        )


class ExaminationDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Examination

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        exam: Examination = self.get_object()
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:section-detail", kwargs={"pk": self.get_object().section.pk}
        )


class ExaminationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Examination

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        exam: Examination = self.get_object()
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        exam: Examination = context_data["object"]
        context_data["questions"] = ExamQuestion.objects.filter(exam=exam)
        return context_data


class ExamQuestionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = ExamQuestion
    fields = ["question_text", "score"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        exam: Examination = get_object_or_404(
            Examination, id=getattr(request, request.method)["exam_id"]
        )
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["exam_id"] = getattr(self.request, self.request.method)["exam_id"]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        question: ExamQuestion = form.instance
        question.exam = Examination.objects.get(
            id=getattr(self.request, self.request.method)["exam_id"]
        )
        question.question_no = 1
        query_set = ExamQuestion.objects.filter(exam=question.exam)
        if query_set:
            question.content_no += query_set.aggregate(Max("question_no"))[
                "question_no__max"
            ]

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:examination-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["exam_id"]},
        )


class ExamQuestionUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = ExamQuestion
    fields = ["question_text", "score"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: ExamQuestion = self.get_object()
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:exam_question-detail", kwargs={"pk": self.get_object().pk}
        )


class ExamQuestionDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = ExamQuestion

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: ExamQuestion = self.get_object()
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:examination-detail", kwargs={"pk": self.get_object().exam.pk}
        )


class ExamQuestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExamQuestion

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: ExamQuestion = self.get_object()
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        question: ExamQuestion = context_data["object"]
        context_data["choices"] = ExamQuestionChoice.objects.filter(question=question)
        return context_data


class ExamQuestionChoiceCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = ExamQuestionChoice
    fields = ["choice_text", "correct_answer_flag"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: ExamQuestion = get_object_or_404(
            ExamQuestion, id=getattr(request, request.method)["question_id"]
        )
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["question_id"] = getattr(self.request, self.request.method)[
            "question_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        choice: ExamQuestionChoice = form.instance
        choice.question = ExamQuestion.objects.get(
            id=getattr(self.request, self.request.method)["question_id"]
        )
        choice.choice_no = 1
        query_set = ExamQuestionChoice.objects.filter(question=choice.question)
        if query_set:
            choice.choice_no += query_set.aggregate(Max("choice_no"))["choice_no__max"]

        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:exam_question-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["question_id"]},
        )


class ExamQuestionChoiceUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = ExamQuestionChoice
    fields = ["choice_text", "correct_answer_flag"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        choice: ExamQuestionChoice = self.get_object()
        question: ExamQuestion = choice.question
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:exam_question_choice-detail", kwargs={"pk": self.get_object().pk}
        )


class ExamQuestionChoiceDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = ExamQuestionChoice

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        choice: ExamQuestionChoice = self.get_object()
        question: ExamQuestion = choice.question
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:exam_question-detail", kwargs={"pk": self.get_object().question.pk}
        )


class ExamQuestionChoiceDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExamQuestionChoice

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        choice: ExamQuestionChoice = self.get_object()
        question: ExamQuestion = choice.question
        exam: Examination = question.exam
        section: Section = exam.section
        course: Course = section.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)


class CouponCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Coupon
    fields = [
        "discount_rate",
        "discount_amount",
        "applying_start_date",
        "applying_end_date",
        "available_count",
    ]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        course: Course = get_object_or_404(
            Course, id=getattr(request, request.method)["course_id"]
        )
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["course"] = Course.objects.get(id=self.request.GET["course_id"])
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        coupon: Coupon = form.instance
        coupon.course = Course.objects.get(
            id=getattr(self.request, self.request.method)["course_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:course-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["course_id"]},
        )


class CouponUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Coupon
    fields = [
        "discount_rate",
        "discount_amount",
        "applying_start_date",
        "applying_end_date",
        "available_count",
    ]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        coupon: Coupon = self.get_object()
        course: Course = coupon.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        coupon: Coupon = context_data["object"]
        context_data["course"] = coupon.course
        return context_data

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:coupon-detail", kwargs={"pk": self.get_object().pk}
        )


class CouponDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Coupon

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        coupon: Coupon = self.get_object()
        course: Course = coupon.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "teacher:course-detail", kwargs={"pk": self.get_object().course.pk}
        )


class CouponDetailView(LoginRequiredMixin, generic.DetailView):
    model = Coupon

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        coupon: Coupon = self.get_object()
        course: Course = coupon.course
        teacher: Teacher = course.teacher
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)


class CommentCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Comment
    fields = ["comment_text"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: Question = Question.objects.get(
            id=getattr(request, request.method)["question_id"]
        )
        teacher: Teacher = question.content.section.course.teacher
        if teacher.user_ptr != request.user:
            raise PermissionDenied("You do not have permission to comment.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["question_id"] = getattr(self.request, self.request.method)[
            "question_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        comment: Comment = form.instance
        comment.question = Question.objects.get(
            id=getattr(self.request, self.request.method)["question_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        question: Question = Question.objects.get(
            id=getattr(self.request, self.request.method)["question_id"]
        )
        content: Content = question.content
        return reverse_lazy(
            (
                "examination-detail"
                if content.content_flag
                else "teacher:lecture_video-detail"
            ),
            kwargs={"pk": question.content.id},
        )