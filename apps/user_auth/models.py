from django.db import models
from apps.main.models import BaseModel
from django.contrib.auth.models import User


class OTP(BaseModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='auth_process'
    )
    otp_code = models.CharField(
        max_length=6,
    )

    def is_otp_valid(self, otp):
        return self.otp == otp

    def __str__(self):
        return f"{self.otp_code} / {self.user}"


class MorshedStudent(BaseModel):
    morshed_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='morshed_student'
    )
    student_id = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    student_gpa = models.FloatField(
        null=True,
        blank=True
    )
    student_major = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )
    student_phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    student_address = models.TextField(
        null=True,
        blank=True
    )

    USERNAME_FIELD = 'student_id'

    def get_username(self):
        return self.student_id

    def __str__(self):
        return f"{self.student_id} / {self.morshed_user.first_name} {self.morshed_user.last_name}"
