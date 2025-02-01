from asyncio.format_helpers import _format_callback
from django.db.models import Max
from django.forms.models import BaseModelForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, get_object_or_404
from .forms import (
    CurriculumExamForm,
    CurriculumGroupForm,
    GroupCurriculumForm,
    GroupStudentForm,
)
from .models import (
    Company,
    CorporateAttendingStudent,
    Group,
    TrainingCurriculum,
    TrainingCurriculumCourse,
    GroupStudent,
    GroupCurriculum,
    CorporateAttendingStudentCurriculum,
    TrainingCurriculumExam,
)


# Create your views here.
class CompanyListView(generic.ListView):
    model = Company


class CompanyCreateView(generic.edit.CreateView):
    model = Company
    fields = ["company_name"]

    def get_success_url(self) -> str:
        return reverse_lazy("company:index")


class CompanyUpdateView(generic.edit.UpdateView):
    model = Company
    fields = ["company_name"]

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail", kwargs={"pk": self.get_object().pk}
        )


class CompanyDeleteView(generic.edit.DeleteView):
    model = Company

    def get_success_url(self) -> str:
        return reverse_lazy("company:index")


class CompanyDetailView(generic.DetailView):
    model = Company

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["students"] = CorporateAttendingStudent.objects.filter(
            company=context_data["object"]
        )
        context_data["groups"] = Group.objects.filter(company=context_data["object"])
        context_data["curriculums"] = TrainingCurriculum.objects.filter(
            company=context_data["object"]
        )
        return context_data


class CorporateAttendingStudentCreateView(generic.edit.CreateView):
    model = CorporateAttendingStudent
    fields = ["username"]

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["company_id"] = getattr(self.request, self.request.method)[
            "company_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        student: CorporateAttendingStudent = form.instance
        student.company = get_object_or_404(
            Company, pk=getattr(self.request, self.request.method)["company_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class CorporateAttendingStudentUpdateView(generic.edit.UpdateView):
    model = CorporateAttendingStudent
    fields = ["username"]

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:corporate_attending_student-detail",
            kwargs={"pk": self.get_object().pk},
        )


class CorporateAttendingStudentDeleteView(generic.edit.DeleteView):
    model = CorporateAttendingStudent

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class CorporateAttendingStudentDetailView(generic.DetailView):
    model = CorporateAttendingStudent

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        student: CorporateAttendingStudent = context_data["object"]
        groups = GroupStudent.objects.filter(student=student)
        context_data["groups"] = groups
        print(groups.query)
        curriculums = GroupCurriculum.objects.filter(group_id__in=groups.values("group_id"))
        context_data["curriculums"] = curriculums
        print(curriculums.query)
        return context_data


class GroupCreateView(generic.edit.CreateView):
    model = Group
    fields = ["group_name"]

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["company_id"] = getattr(self.request, self.request.method)[
            "company_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        group: Group = form.instance
        group.company = get_object_or_404(
            Company, pk=getattr(self.request, self.request.method)["company_id"]
        )
        query_set = Group.objects.filter(company=group.company)
        group.group_no = 1
        if query_set:
            group.group_no += query_set.aggregate(Max("group_no"))["group_no__max"]
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class GroupUpdateView(generic.edit.UpdateView):
    model = Group
    fields = ["group_name"]

    def get_success_url(self) -> str:
        return reverse_lazy("company:group-detail", kwargs={"pk": self.get_object().pk})


class GroupDeleteView(generic.edit.DeleteView):
    model = Group

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class GroupDetailView(generic.DetailView):
    model = Group

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        group: Group = context_data["object"]
        context_data["students"] = GroupStudent.objects.filter(group=group)
        context_data["curriculums"] = GroupCurriculum.objects.filter(group=group)
        return context_data


class TrainingCurriculumCreateView(generic.edit.CreateView):
    model = TrainingCurriculum
    fields = ["training_curriculum_name"]

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        context_data["company_id"] = getattr(self.request, self.request.method)[
            "company_id"
        ]
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        curriculum: TrainingCurriculum = form.instance
        curriculum.company = get_object_or_404(
            Company, pk=getattr(self.request, self.request.method)["company_id"]
        )
        query_set = TrainingCurriculum.objects.filter(company=curriculum.company)
        curriculum.training_curriculum_no = 1
        if query_set:
            curriculum.training_curriculum_no += query_set.aggregate(
                Max("training_curriculum_no")
            )["training_curriculum_no__max"]
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class TrainingCurriculumUpdateView(generic.edit.UpdateView):
    model = TrainingCurriculum
    fields = ["training_curriculum_name"]

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail", kwargs={"pk": self.get_object().pk}
        )


class TrainingCurriculumDeleteView(generic.edit.DeleteView):
    model = TrainingCurriculum

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:company-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["company_id"]},
        )


class TrainingCurriculumDetailView(generic.DetailView):
    model = TrainingCurriculum

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        curriculum = context_data["object"]
        context_data["courses"] = TrainingCurriculumCourse.objects.filter(
            curriculum=curriculum
        )
        context_data["groups"] = GroupCurriculum.objects.filter(curriculum=curriculum)
        context_data["students"] = CorporateAttendingStudentCurriculum.objects.filter(
            curriculum=curriculum
        )
        context_data["exams"] = TrainingCurriculumExam.objects.filter(
            curriculum=curriculum
        )
        return context_data


class CurriculumCourseCreateView(generic.edit.CreateView):
    model = TrainingCurriculumCourse
    fields = ["course"]

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        curriculum: TrainingCurriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        context_data["curriculum"] = curriculum
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        curriculum_course: TrainingCurriculumCourse = form.instance
        curriculum_course.curriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        curriculum_course.attending_order = 1
        query_set = TrainingCurriculumCourse.objects.filter(
            curriculum=curriculum_course.curriculum
        )
        if query_set:
            curriculum_course.attending_order += query_set.aggregate(
                Max("attending_order")
            )["attending_order__max"]
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["curriculum_id"]},
        )


class CurriculumCourseUpdateView(generic.edit.UpdateView):
    model = TrainingCurriculumCourse
    fields = "__all__"


class CurriculumCourseDeleteView(generic.edit.DeleteView):
    model = TrainingCurriculumCourse

    def form_valid(self, form):
        curriculum_course: TrainingCurriculumCourse = self.get_object()
        response: HttpResponseRedirect = super().form_valid(form)
        courses = TrainingCurriculumCourse.objects.filter(
            curriculum=curriculum_course.curriculum,
            attending_order__gt=curriculum_course.attending_order,
        )
        for course in courses:
            course.attending_order -= 1
            course.save()
        return response

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail",
            kwargs={"pk": self.get_object().curriculum.pk},
        )


class CurriculumCourseDetailView(generic.DetailView):
    model = TrainingCurriculumCourse


class GroupStudentCreateView(generic.edit.CreateView):
    form_class = GroupStudentForm
    template_name = "company/groupstudent_form.html"

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        context_data["group"] = get_object_or_404(
            Group, pk=getattr(self.request, self.request.method)["group_id"]
        )
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        group_student: GroupStudent = form.instance
        group_student.group = get_object_or_404(
            Group, pk=getattr(self.request, self.request.method)["group_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:group-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["group_id"]},
        )


class GroupStudentUpdateView(generic.edit.UpdateView):
    model = GroupStudent
    fields = "__all__"


class GroupStudentDeleteView(generic.edit.DeleteView):
    model = GroupStudent

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:group-detail",
            kwargs={"pk": self.get_object().group.pk},
        )


class GroupStudentDetailView(generic.DetailView):
    model = GroupStudent


class GroupCurriculumCreateView(generic.edit.CreateView):
    form_class = GroupCurriculumForm
    template_name = "company/groupcurriculum_form.html"

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        group: Group = get_object_or_404(
            Group, pk=getattr(self.request, self.request.method)["group_id"]
        )
        context_data["group"] = group
        context_data["curriculum"] = None
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        group_curriculum: GroupCurriculum = form.instance
        group_curriculum.group = get_object_or_404(
            Group, pk=getattr(self.request, self.request.method)["group_id"]
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:group-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["group_id"]},
        )


class CurriculumGroupCreateView(generic.edit.CreateView):
    form_class = CurriculumGroupForm
    template_name = "company/groupcurriculum_form.html"

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        curriculum: TrainingCurriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        context_data["curriculum"] = curriculum
        context_data["group"] = None
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        group_curriculum: GroupCurriculum = form.instance
        group_curriculum.curriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["curriculum_id"]},
        )


class GroupCurriculumUpdateView(generic.edit.UpdateView):
    model = GroupCurriculum
    fields = ["date_startable_attending", "attending_complete_deadline_date"]

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:group_curriculum-detail",
            kwargs={"pk": self.get_object().pk},
        )


class GroupCurriculumDeleteView(generic.edit.DeleteView):
    model = GroupCurriculum

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:group-detail",
            kwargs={"pk": self.get_object().group.pk},
        )


class CurriculumGroupDeleteView(generic.edit.DeleteView):
    model = GroupCurriculum

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:curriculum-detail",
            kwargs={"pk": self.get_object().curriculum.pk},
        )


class GroupCurriculumDetailView(generic.DetailView):
    model = GroupCurriculum


class StudentCurriculumCreateView(generic.edit.CreateView):
    model = CorporateAttendingStudentCurriculum
    fields = "__all__"


class StudentCurriculumUpdateView(generic.edit.UpdateView):
    model = CorporateAttendingStudentCurriculum
    fields = "__all__"


class StudentCurriculumDeleteView(generic.edit.DeleteView):
    model = CorporateAttendingStudentCurriculum


class StudentCurriculumDetailView(generic.DetailView):
    model = CorporateAttendingStudentCurriculum


class CurriculumExamCreateView(generic.edit.CreateView):
    form_class = CurriculumExamForm
    template_name = "company/trainingcurriculumexam_form.html"

    def get_context_data(self, **kwargs) -> dict:
        context_data = super().get_context_data(**kwargs)
        curriculum: TrainingCurriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        context_data["curriculum"] = curriculum
        return context_data

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        curriculum_exam: TrainingCurriculumExam = form.instance
        curriculum_exam.curriculum = get_object_or_404(
            TrainingCurriculum,
            pk=getattr(self.request, self.request.method)["curriculum_id"],
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail",
            kwargs={"pk": getattr(self.request, self.request.method)["curriculum_id"]},
        )


class CurriculumExamUpdateView(generic.edit.UpdateView):
    model = TrainingCurriculumExam
    fields = ["passing_base_point"]

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        curriculum_exam: TrainingCurriculumExam = self.get_object()
        context_data["curriculum"] = curriculum_exam.curriculum
        return context_data


class CurriculumExamDeleteView(generic.edit.DeleteView):
    model = TrainingCurriculumExam

    def get_success_url(self) -> str:
        return reverse_lazy(
            "company:training_curriculum-detail",
            kwargs={"pk": self.get_object().curriculum.pk},
        )


class CurriculumExamDetailView(generic.DetailView):
    model = TrainingCurriculumExam
