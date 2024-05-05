from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.models import MorshedStudent
from apps.course.constant import COURSE_LEVEL


class Courses(BaseModel):
    course_name = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    course_number = models.IntegerField(
        null=True,
        blank=True
    )
    course_image = models.ImageField(
        upload_to='media/course_images/',
        null=True,
        blank=True
    )
    course_description = models.TextField(
        null=True,
        blank=True
    )
    is_external = models.BooleanField(
        default=False
    )
    course_grade = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    course_price = models.FloatField(
        null=True,
        blank=True
    )
    course_provider = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    course_url = models.URLField(
        null=True,
        blank=True
    )
    course_level = models.CharField(
        max_length=100,
        choices=COURSE_LEVEL,
        null=True,
        blank=True
    )
    number_of_hours = models.IntegerField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.course_name} / {self.course_number}"


class StudentCourse(BaseModel):
    course_id = models.ForeignKey(
        Courses,
        on_delete=models.CASCADE,
        related_name='course_student'
    )
    student_id = models.ForeignKey(
        MorshedStudent,
        on_delete=models.CASCADE,
        related_name='student_course'
    )
    is_completed = models.BooleanField(
        default=False
    )

    def __str__(self):
        return f"{self.course_id} / {self.student_id}"

