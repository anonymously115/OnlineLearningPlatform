from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Account(User):
    teacher_flag = models.BooleanField(default=False)
    student_flag = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Teacher(Account):
    profile = models.TextField(verbose_name="講師プロフィール")


class Student(Account):
    pay_info = models.TextField(verbose_name="支払情報")
