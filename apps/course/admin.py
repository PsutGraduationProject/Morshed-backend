from django.contrib import admin
from apps.course.models import (
    Courses,
    StudentCourse
)

admin.site.register(Courses)
admin.site.register(StudentCourse)
