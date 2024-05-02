from django.db import models
from apps.main.models import BaseModel
from apps.user_auth.manager import MorshedStudentManager
from django.contrib.auth.models import (
    AbstractUser,
)


class MorshedStudent(BaseModel, AbstractUser):
    groups = None
    user_permissions = None
    last_login = None
    date_joined = None

    objects = MorshedStudentManager()

    student_id = models.IntegerField(
        unique=True
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

    def __str__(self):
        return f"{self.student_id} / {self.first_name} {self.last_name}"


class OTP(BaseModel):
    morshed_user = models.ForeignKey(
        MorshedStudent,
        on_delete=models.CASCADE,
        related_name='auth_process'
    )
    otp_code = models.CharField(
        max_length=6,
    )

    def is_otp_valid(self, otp):
        return self.otp == otp

    def __str__(self):
        return f"{self.morshed_user} / {self.otp_code}"
