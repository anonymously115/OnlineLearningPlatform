from django import forms
from .models import CoursePurchase
from teacher.models import Coupon
from django.db.models import Count, F
from django.db.models.functions import Coalesce
from django.utils import timezone


class CoursePurchaseForm(forms.ModelForm):
    class Meta:
        model = CoursePurchase
        fields = ["coupon", "flag"]

    def __init__(self, data, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        today = timezone.now().date()
        """
        SELECT
            a.*,
            IFNULL(b.used_count, 0) AS used_count
        FROM
            teacher_coupon AS a
            LEFT OUTER JOIN (
                SELECT
                    coupon_id,
                    COUNT(*) AS used_count
                FROM
                    student_coursepurchase
                GROUP BY
                    coupon_id
            ) AS b ON a.id = b.coupon_id
        WHERE
            course_id = data['course_id']
            AND applying_start_date <= date('now')
            AND date('now') <= applying_end_date
            AND available_count >= IFNULL(b.used_count, 0);
        """
        self.fields["coupon"].queryset = Coupon.objects.annotate(
            used_count=Coalesce(Count("coursepurchase"), 0)
        ).filter(
            course_id=data["course_id"],
            applying_start_date__lte=today,
            applying_end_date__gte=today,
            available_count__gt=F("used_count"),
        )


class ExamResultDetailForm(forms.Form):
    choice = forms.MultipleChoiceField(widget=forms.RadioSelect())