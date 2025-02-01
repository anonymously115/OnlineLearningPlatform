from django.db import models
from online_learning_platform.models import Student
from teacher.models import Course, Examination


# Create your models here.
class Company(models.Model):
    company_name = models.CharField(verbose_name="企業名", max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.company_name


class TrainingCurriculum(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    training_curriculum_no = models.IntegerField()
    training_curriculum_name = models.CharField(
        verbose_name="研修カリキュラム名", max_length=15
    )
    courses = models.ManyToManyField(
        Course, through="TrainingCurriculumCourse", verbose_name="コース"
    )
    exams = models.ManyToManyField(
        Examination, through="TrainingCurriculumExam", verbose_name="テスト"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.training_curriculum_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "training_curriculum_no"],
                name="unique_training_curriculum",
            )
        ]


class CorporateAttendingStudent(Student):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    curriculums = models.ManyToManyField(
        TrainingCurriculum,
        through="CorporateAttendingStudentCurriculum",
        verbose_name="研修カリキュラム",
        related_name="corporate_attending_student",
    )


class Group(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    group_no = models.IntegerField()
    group_name = models.CharField(verbose_name="グループ名", max_length=15)
    students = models.ManyToManyField(
        CorporateAttendingStudent, through="GroupStudent", verbose_name="法人受講生"
    )
    curriculums = models.ManyToManyField(
        TrainingCurriculum, through="GroupCurriculum", verbose_name="研修カリキュラム"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.group_name

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["company", "group_no"],
                name="unique_group",
            )
        ]


class TrainingCurriculumCourse(models.Model):
    curriculum = models.ForeignKey(TrainingCurriculum, on_delete=models.RESTRICT)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    attending_order = models.IntegerField(verbose_name="受講順")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "course"],
                name="unique_curriculumcourse",
            ),
            models.UniqueConstraint(
                fields=["curriculum", "attending_order"],
                name="unique_curriculumcourse_order",
            ),
        ]


class GroupStudent(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    student = models.ForeignKey(CorporateAttendingStudent, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "student"],
                name="unique_groupstudent",
            )
        ]


class GroupCurriculum(models.Model):
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)
    curriculum = models.ForeignKey(TrainingCurriculum, on_delete=models.RESTRICT)
    date_startable_attending = models.DateField(verbose_name="受講開始可能年月日")
    attending_complete_deadline_date = models.DateField(
        verbose_name="受講完了期限年月日"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "curriculum"],
                name="unique_groupcurriculum",
            )
        ]


class CorporateAttendingStudentCurriculum(models.Model):
    student = models.ForeignKey(CorporateAttendingStudent, on_delete=models.RESTRICT)
    curriculum = models.ForeignKey(TrainingCurriculum, on_delete=models.RESTRICT)
    training_curriculum_attending_start_time = models.DateTimeField(auto_now_add=True)
    training_curriculum_attending_complete_time = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["student", "curriculum"],
                name="unique_studentcurriculum",
            )
        ]


class TrainingCurriculumExam(models.Model):
    curriculum = models.ForeignKey(TrainingCurriculum, on_delete=models.RESTRICT)
    exam = models.ForeignKey(Examination, on_delete=models.RESTRICT)
    passing_base_point = models.IntegerField(verbose_name="合格基準点")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["curriculum", "exam"],
                name="unique_curriculumexam",
            )
        ]
