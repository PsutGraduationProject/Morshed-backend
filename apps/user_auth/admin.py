from django.contrib import admin
from apps.user_auth.models import (
    MorshedStudent,
    OTP,
)

admin.site.register(MorshedStudent)
admin.site.register(OTP)
