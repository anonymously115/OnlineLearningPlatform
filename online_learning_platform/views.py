from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models.base import Model
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic
from .models import Account, Teacher, Student


# Create your views here.
class AccountDetailView(LoginRequiredMixin, generic.DetailView):
    model = Account

    def get_object(self) -> Model:
        if not self.request.user.is_authenticated:
            return self.model()
        queryset = self.model.objects.filter(user_ptr=self.request.user)
        if queryset.count():
            return queryset.get()
        account: Account = self.model(user_ptr=self.request.user)
        account.created_at = datetime.now()
        account.updated_at = datetime.now()
        account.save_base(raw=True)
        account = Account.objects.get(user_ptr=self.request.user)
        account.save()
        return account

    def get_context_data(self, **kwargs) -> dict:
        context_data: dict = super().get_context_data(**kwargs)
        account: Account = context_data["object"]
        context_data["teacher"] = (
            Teacher.objects.get(account_ptr=account)
            if account.teacher_flag
            else Teacher(account_ptr=account)
        )
        context_data["student"] = (
            Student.objects.get(account_ptr=account)
            if account.student_flag
            else Student(account_ptr=account)
        )
        return context_data


class TeacherCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Teacher
    fields = ["profile"]

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        teacher: Teacher = form.instance
        queryset = Account.objects.filter(user_ptr=self.request.user)
        account: Account = (
            queryset.get() if queryset.count() else Account(user_ptr=self.request.user)
        )
        account.teacher_flag = True
        account.save_base(raw=True)
        account = Account.objects.get(user_ptr=self.request.user)
        teacher.account_ptr = account
        teacher.save_base(raw=True)
        teacher = self.model.objects.get(account_ptr=account)
        form.instance = teacher
        return super().form_valid(form)


class TeacherUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Teacher
    fields = ["profile"]

    def get_object(self) -> Model:
        return self.model.objects.get(user_ptr=self.request.user)

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        teacher: Teacher = self.get_object()
        if teacher.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")


class TeacherDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Teacher

    def get_object(self) -> Model:
        return self.model.objects.get(user_ptr=self.request.user)

    def form_valid(self, form):
        teacher: Teacher = self.object
        teacher.teacher_flag = False
        teacher.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")


class StudentCreateView(LoginRequiredMixin, generic.edit.CreateView):
    model = Student
    fields = ["pay_info"]

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        student: Student = form.instance
        queryset = Account.objects.filter(user_ptr=self.request.user)
        account: Account = (
            queryset.get() if queryset.count() else Account(user_ptr=self.request.user)
        )
        account.student_flag = True
        account.save_base(raw=True)
        account = Account.objects.get(user_ptr=self.request.user)
        student.account_ptr = account
        student.save_base(raw=True)
        student = self.model.objects.get(account_ptr=account)
        form.instance = student
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")


class StudentUpdateView(LoginRequiredMixin, generic.edit.UpdateView):
    model = Student
    fields = ["pay_info"]

    def get_object(self) -> Model:
        return self.model.objects.get(user_ptr=self.request.user)

    def dispatch(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        student: Student = self.get_object()
        if student.user_ptr != self.request.user:
            raise PermissionDenied("You do not have permission to edit.")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")


class StudentDeleteView(LoginRequiredMixin, generic.edit.DeleteView):
    model = Student

    def get_object(self) -> Model:
        return self.model.objects.get(user_ptr=self.request.user)

    def form_valid(self, form):
        student: Student = self.object
        student.student_flag = False
        student.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self) -> str:
        return reverse_lazy("online_learning_platform:index")
