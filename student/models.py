from tabnanny import verbose
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy
from online_learning_platform.models import Student
from teacher.models import (
    Content,
    Coupon,
    Course,
    ExamQuestion,
    ExamQuestionChoice,
    Section,
)


# Create your models here.
class CoursePurchase(models.Model):
    def validate_true(value):
        if not value:
            raise ValidationError("Check the box.")
            # raise ValidationError(
            #     gettext_lazy("%(value) is not True"),
            #     params={"value": value},
            # )

    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    purchase_date = models.DateField(auto_now_add=True)
    purchase_price = models.IntegerField()
    coupon = models.ForeignKey(Coupon, blank=True, null=True, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    flag = models.BooleanField(validators=[validate_true])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "student"], name="unique_course_purchase"
            )
        ]


class CourseAttending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    start_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(null=True)
    five_stage_rating = models.IntegerField(
        verbose_name="５段階評価", choices={i: i for i in range(1, 6)}, null=True
    )
    feedback = models.TextField(verbose_name="感想", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "course"], name="unique_course_attending"
            )
        ]


class SectionAttending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    section = models.ForeignKey(Section, on_delete=models.RESTRICT)
    start_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "section"], name="unique_section_attending"
            )
        ]


class ContentAttending(models.Model):
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    content = models.ForeignKey(Content, on_delete=models.RESTRICT)
    start_time = models.DateTimeField(auto_now_add=True)
    complete_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "content"], name="unique_content_attending"
            )
        ]


class ExamResult(ContentAttending):
    high_score = models.IntegerField(null=True)


class ExamResultDetail(models.Model):
    result = models.ForeignKey(ExamResult, on_delete=models.CASCADE)
    question = models.ForeignKey(ExamQuestion, on_delete=models.RESTRICT)
    choice = models.ForeignKey(ExamQuestionChoice, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["result", "question"], name="unique_exam_result_detail"
            )
        ]


class ExamResultHistory(models.Model):
    result = models.ForeignKey(ExamResult, on_delete=models.CASCADE)
    exam_execution_time = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["result", "exam_execution_time"],
                name="unique_exam_result_history",
            )
        ]


class Question(models.Model):
    content = models.ForeignKey(Content, on_delete=models.RESTRICT)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    question_title = models.CharField(verbose_name="質問タイトル", max_length=15)
    question_text = models.TextField(verbose_name="質問文")
    question_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question_title


class Comment(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE,related_name="comment_set")
    comment_text = models.TextField(verbose_name="コメント文")
    comment_time = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.comment_text