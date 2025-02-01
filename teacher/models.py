from typing import Collection
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from online_learning_platform.models import Teacher

# Create your models here.
class Course(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_name = models.CharField(verbose_name="コース名", max_length=15)
    standard_price = models.IntegerField(
        verbose_name="標準価格", validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.course_name


class Section(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section_no = models.IntegerField()
    section_name = models.CharField(verbose_name="セクション名", max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.section_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["course", "section_no"], name="unique_section"
            )
        ]


class Content(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    content_no = models.IntegerField()
    content_name = models.CharField(verbose_name="コンテンツ名", max_length=15)
    content_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.content_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["section", "content_no"], name="unique_content"
            )
        ]


class LectureVideo(Content):
    lecture_time = models.IntegerField(
        verbose_name="講義時間", validators=[MinValueValidator(0)]
    )


class Examination(Content):
    answer_limit_time = models.IntegerField(
        verbose_name="解答制限時間", validators=[MinValueValidator(0)]
    )


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Examination, on_delete=models.CASCADE)
    question_no = models.IntegerField()
    question_text = models.TextField(
        verbose_name="設問文",
    )
    score = models.IntegerField(verbose_name="配点", validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.question_text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["exam", "question_no"], name="unique_exam_question"
            )
        ]


class ExamQuestionChoice(models.Model):
    question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
    choice_no = models.IntegerField()
    choice_text = models.TextField(
        verbose_name="選択文",
    )
    correct_answer_flag = models.BooleanField(
        verbose_name="正解フラグ",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.choice_text

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["question", "choice_no"], name="unique_exam_question_choice"
            )
        ]


class Coupon(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    discount_rate = models.DecimalField(
        verbose_name="割引率(％)",
        blank=True,
        null=True,
        max_digits=18,
        decimal_places=16,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    discount_amount = models.IntegerField(
        verbose_name="値引額", blank=True, null=True, validators=[MinValueValidator(0)]
    )
    applying_start_date = models.DateField(
        verbose_name="適用開始年月日(Y-m-d)",
    )
    applying_end_date = models.DateField(
        verbose_name="適用終了年月日(Y-m-d)",
    )
    available_count = models.IntegerField(
        verbose_name="使用可能人数",
        validators=[MinValueValidator(0), MaxValueValidator(1000)],
    )
    coupon_issuing_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_clean(
        self,
        exclude: Collection[str] | None = ...,
        validate_unique: bool = ...,
        validate_constraints: bool = ...,
    ) -> None:
        errors = {}
        try:
            return super().full_clean(exclude, validate_unique, validate_constraints)
        except ValidationError as e:
            errors = e.update_error_dict(errors)
        # if self.discount_amount and "discount_amount" not in errors:
        #     if self.discount_amount > self.course.standard_price:
        #         errors["discount_amount"] = ValidationError("値引額は標準価格以下でなければなりません。")
        if "applying_start_date" not in errors and "applying_end_date" not in errors:
            if self.applying_start_date and self.applying_end_date:
                if self.applying_start_date > self.applying_end_date:
                    errors["applying_start_date"] = ValidationError(
                        "適用開始年月日は適用終了年月日以降でなければなりません。"
                    )
                    errors["applying_end_date"] = ValidationError(
                        "適用終了年月日は適用開始年月日以降でなければなりません。"
                    )
        if errors:
            raise ValidationError(errors)

    def __str__(self) -> str:
        s = ""
        if self.discount_rate:
            s += f"{self.discount_rate}".rstrip("0").rstrip(".") + "%"
            if self.discount_amount:
                s += " and "
        if self.discount_amount:
            s += f"{self.discount_amount}"
        if s:
            s += " OFF"
        return s
