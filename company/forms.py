
from typing import Any, Mapping
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from django.shortcuts import get_object_or_404
from .models import (
    Company,
    CorporateAttendingStudent,
    Group,
    GroupStudent,
    TrainingCurriculum,
    GroupCurriculum,
    TrainingCurriculumCourse,
    TrainingCurriculumExam,
)
from teacher.models import Examination, Section


class GroupCurriculumForm(forms.ModelForm):
    class Meta:
        model = GroupCurriculum
        exclude = ["group"]

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        group: Group = get_object_or_404(Group, pk=self.data["group_id"])
        self.fields["curriculum"].queryset = TrainingCurriculum.objects.filter(
            company=group.company
        )


class CurriculumGroupForm(forms.ModelForm):
    class Meta:
        model = GroupCurriculum
        exclude = ["curriculum"]

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        curriculum: TrainingCurriculum = get_object_or_404(
            TrainingCurriculum, pk=self.data["curriculum_id"]
        )
        self.fields["group"].queryset = Group.objects.filter(company=curriculum.company)


class GroupStudentForm(forms.ModelForm):
    class Meta:
        model = GroupStudent
        exclude = ["group"]

    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(data, *args, **kwargs)
        group: Group = get_object_or_404(Group, pk=self.data["group_id"])
        self.fields["student"].queryset = CorporateAttendingStudent.objects.filter(
            company=group.company
        )


class CurriculumExamForm(forms.ModelForm):
    class Meta:
        model = TrainingCurriculumExam
        exclude = ["curriculum"]

    def __init__(self, data, *args, **kwargs) -> None:
        super().__init__(data, args, kwargs)
        courses = TrainingCurriculumCourse.objects.filter(
            curriculum_id=self.data["curriculum_id"]
        )
        sections = Section.objects.filter(course_id__in=courses.values("course_id"))
        exams = Examination.objects.filter(section__in=sections)
        self.fields["exam"].queryset = exams
