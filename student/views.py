from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.base import Model
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from online_learning_platform.models import Account, Student
from teacher.models import (
    Content,
    Course,
    Section,
    ExamQuestion,
    ExamQuestionChoice,
)
from .forms import CoursePurchaseForm, ExamResultDetailForm
from .models import (
    Comment,
    ContentAttending,
    CourseAttending,
    CoursePurchase,
    ExamResult,
    ExamResultDetail,
    ExamResultHistory,
    Question,
    SectionAttending,
)


# Create your views here.
class StudentDetailView(LoginRequiredMixin, generic.DetailView):
    model = Student

    def get_object(self) -> Model:
        return self.model.objects.get(
            account_ptr=Account.objects.get(user_ptr=self.request.user)
        )

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        student: Student = context_data["object"]
        purchased = CoursePurchase.objects.filter(student=student)
        context_data["purchased"] = purchased
        context_data["courses"] = Course.objects.exclude(
            id__in=purchased.values("course_id")
        )
        return context_data


class CourseIndexView(LoginRequiredMixin, generic.ListView):
    model = Course


class CoursePurchaseCreateView(LoginRequiredMixin, generic.edit.CreateView):
    # model = CoursePurchase
    # fields = ["coupon", "flag"]
    form_class = CoursePurchaseForm
    template_name = "student/coursepurchase_form.html"

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["course"] = Course.objects.get(
            id=getattr(self.request, self.request.method)["course_id"]
        )
        context_data["sections"] = Section.objects.filter(
            course_id=getattr(self.request, self.request.method)["course_id"]
        )
        query_set = CoursePurchase.objects.filter(
            course_id=getattr(self.request, self.request.method)["course_id"],
            student_id=self.request.user.id,
        )
        context_data["purchased"] = True if query_set else False
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        purchase: CoursePurchase = form.instance
        purchase.course = Course.objects.get(
            id=getattr(self.request, self.request.method)["course_id"]
        )
        purchase.purchase_price = purchase.course.standard_price
        if purchase.coupon:
            purchase.purchase_price = int(
                (
                    purchase.course.standard_price
                    * (100 - purchase.coupon.discount_rate)
                    - purchase.coupon.discount_amount
                )
                / 100
            )
        purchase.student = Student.objects.get(user_ptr=self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("student:index")


class CoursePurchaseDetailView(LoginRequiredMixin, generic.DetailView):
    model = CoursePurchase

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        purchase: CoursePurchase = self.get_object()
        student: Student = purchase.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        purchase: CoursePurchase = context_data["object"]
        query_set = CourseAttending.objects.filter(
            student=purchase.student, course=purchase.course
        )
        context_data["attending"] = query_set.get() if query_set else None
        context_data["sections"] = Section.objects.filter(course=purchase.course)
        return context_data


class CourseAttendingCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = CourseAttending
    fields = []

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["purchase"] = CoursePurchase.objects.get(
            id=getattr(self.request, self.request.method)["purchase_id"]
        )
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attending: CourseAttending = form.instance
        purchase: CoursePurchase = CoursePurchase.objects.get(
            id=getattr(self.request, self.request.method)["purchase_id"]
        )
        attending.student = purchase.student
        attending.course = purchase.course
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "student:course_purchase-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["purchase_id"]},
        )


class CourseAttendingUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = CourseAttending
    fields = ["five_stage_rating", "feedback"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: CourseAttending = self.get_object()
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        attending: CourseAttending = self.get_object()
        return reverse_lazy(
            "student:course_attending-detail",
            kwargs={"pk": attending.pk},
        )


class CourseAttendingDetailView(LoginRequiredMixin, generic.DetailView):
    model = CourseAttending

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: CourseAttending = self.get_object()
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        attending: CourseAttending = context_data["object"]
        section_attendings = SectionAttending.objects.filter(
            student=attending.student,
            section__in=Section.objects.filter(
                course=Course.objects.get(id=attending.course.id)
            ),
        )
        context_data["attendings"] = section_attendings
        context_data["sections"] = Section.objects.filter(
            course_id=attending.course.id
        ).exclude(id__in=section_attendings.values("section_id"))

        return context_data


class SectionAttendingCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = SectionAttending
    fields = []

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: CourseAttending = get_object_or_404(
            CourseAttending, id=getattr(request, request.method)["course_attending_id"]
        )
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["course_attending"] = CourseAttending.objects.get(
            id=getattr(self.request, self.request.method)["course_attending_id"]
        )
        context_data["section"] = Section.objects.get(
            id=getattr(self.request, self.request.method)["section_id"]
        )
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attending: SectionAttending = form.instance
        course_attending: CourseAttending = CourseAttending.objects.get(
            id=getattr(self.request, self.request.method)["course_attending_id"]
        )
        attending.student = course_attending.student
        attending.section = Section.objects.get(
            id=getattr(self.request, self.request.method)["section_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "student:course_attending-detail",
            kwargs={
                "pk": getattr(self.request, self.request.method)["course_attending_id"]
            },
        )


class SectionAttendingDetailView(LoginRequiredMixin, generic.DetailView):
    model = SectionAttending

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: SectionAttending = self.get_object()
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        attending: SectionAttending = context_data["object"]
        content_attendings = ContentAttending.objects.filter(
            student=attending.student,
            content__in=Content.objects.filter(
                section=Section.objects.get(id=attending.section.id)
            ),
        )
        context_data["attendings"] = content_attendings
        context_data["contents"] = Content.objects.filter(
            section_id=attending.section.id
        ).exclude(id__in=content_attendings.values("content_id"))

        return context_data


class ContentAttendingCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = ContentAttending
    fields = []

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: SectionAttending = get_object_or_404(
            SectionAttending,
            id=getattr(request, request.method)["section_attending_id"],
        )
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["section_attending"] = SectionAttending.objects.get(
            id=getattr(self.request, self.request.method)["section_attending_id"]
        )
        context_data["content"] = Content.objects.get(
            id=getattr(self.request, self.request.method)["content_id"]
        )
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        attending: ContentAttending = form.instance
        section_attending: SectionAttending = SectionAttending.objects.get(
            id=getattr(self.request, self.request.method)["section_attending_id"]
        )
        attending.student = section_attending.student
        attending.content = Content.objects.get(
            id=getattr(self.request, self.request.method)["content_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "student:section_attending-detail",
            kwargs={
                "pk": getattr(self.request, self.request.method)["section_attending_id"]
            },
        )


class ContentAttendingDetailView(LoginRequiredMixin, generic.DetailView):
    model = ContentAttending

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: ContentAttending = self.get_object()
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        content_attending: ContentAttending = context_data["object"]
        context_data["questions"] = Question.objects.filter(
            student_id=self.request.user.id, content=content_attending.content
        )
        return context_data


class ExamResultCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = ExamResult
    fields = []

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: SectionAttending = get_object_or_404(
            SectionAttending,
            id=getattr(request, request.method)["section_attending_id"],
        )
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to create.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["section_attending"] = SectionAttending.objects.get(
            id=getattr(self.request, self.request.method)["section_attending_id"]
        )
        context_data["content"] = Content.objects.get(
            id=getattr(self.request, self.request.method)["content_id"]
        )
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        result: ExamResult = form.instance
        section_attending: SectionAttending = SectionAttending.objects.get(
            id=getattr(self.request, self.request.method)["section_attending_id"]
        )
        result.student = section_attending.student
        result.content = Content.objects.get(
            id=getattr(self.request, self.request.method)["content_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        result: ExamResult = ExamResult.objects.get(
            student_id=self.request.user.id,
            content_id=getattr(self.request, self.request.method)["content_id"],
        )

        return reverse_lazy(
            "student:exam_result-detail",
            kwargs={"pk": result.id},
        )


class ExamResultDetailView(LoginRequiredMixin, generic.DetailView):
    model = ExamResult

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        result: ExamResult = self.get_object()
        student: Student = result.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        forms = []
        result: ExamResult = context_data["object"]
        content: Content = result.content
        section_attending: SectionAttending = SectionAttending.objects.get(
            student_id=self.request.user.id, section=content.section
        )
        context_data["section_attending"] = section_attending
        questions = ExamQuestion.objects.filter(exam_id=content.id)
        for question in questions:
            choices = ExamQuestionChoice.objects.filter(question=question)
            form = ExamResultDetailForm()
            form.fields["choice"].label = question.question_text
            form.fields["choice"].choices = [
                (choice.id, choice.choice_text) for choice in choices
            ]
            forms.append(form)
        context_data["forms"] = forms
        return context_data


def answer(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        history: ExamResultHistory = ExamResultHistory()
        history.total_score = 0
        history.result = ExamResult.objects.get(
            student_id=request.user.id, content_id=request.POST["exam_id"]
        )
        for id in request.POST["choice"]:
            choice: ExamQuestionChoice = ExamQuestionChoice.objects.get(id=id)
            question: ExamQuestion = choice.question
            if choice.correct_answer_flag:
                history.total_score += question.score
            query_set = ExamResultDetail.objects.filter(
                result=history.result, question=question
            )
            detail: ExamResultDetail = None
            if query_set:
                detail = query_set.get()
            else:
                detail = ExamResultDetail()
                detail.result = history.result
                detail.question = question
            detail.choice = choice
            detail.save()
        history.save()
        return HttpResponseRedirect(
            reverse_lazy(
                "student:section_attending-detail",
                kwargs={"pk": request.POST["section_attending_id"]},
            )
        )
    else:
        raise Http404()


class QuestionCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Question
    fields = ["question_title", "question_text"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        attending: ContentAttending = get_object_or_404(
            ContentAttending,
            id=getattr(request, request.method)["content_attending_id"],
        )
        student: Student = attending.student
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to question.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["content_attending_id"] = getattr(
            self.request, self.request.method
        )["content_attending_id"]
        attending: ContentAttending = get_object_or_404(
            ContentAttending,
            id=getattr(self.request, self.request.method)["content_attending_id"],
        )
        context_data["content"] = attending.content
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        question: Question = form.instance
        question.student = Student.objects.get(pk=self.request.user)
        question.content = Content.objects.get(id=self.request.POST["content_id"])
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "student:content_attending-detail",
            kwargs={"pk": self.request.POST["content_attending_id"]},
        )


class QuestionUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Question
    fields = ["question_title", "question_text"]

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: Question = self.get_object()
        student: Student = question.student
        if student.user_ptr != request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        question: Question = self.get_object()
        attending: ContentAttending = get_object_or_404(
            ContentAttending, student=question.student, content=question.content
        )
        context_data["content_attending_id"] = attending.id
        context_data["content"] = attending.content
        return context_data

    def get_success_url(self) -> str:
        return reverse_lazy(
            "student:content_attending-detail",
            kwargs={"pk": self.request.POST["content_attending_id"]},
        )


class QuestionDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Question

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: Question = self.get_object()
        student: Student = question.student
        if student.user_ptr != request.user:
            raise PermissionDenied("You do not have permission to delete.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        question: Question = self.get_object()
        attending: ContentAttending = ContentAttending.objects.get(
            student=question.student, content=question.content
        )
        return reverse_lazy(
            "student:content_attending-detail",
            kwargs={"pk": attending.id},
        )


class QuestionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Question

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        question: Question = self.get_object()
        student: Student = question.student
        if student.user_ptr != request.user:
            raise PermissionDenied("You do not have permission to retrieve.")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        question = context_data["object"]
        query_set = Comment.objects.filter(question=question)
        context_data["comment"] = query_set.get() if query_set else None
        return context_data