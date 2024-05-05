import graphene
from django.db.models import Q
from apps.user_auth.models import MorshedStudent
from graphene_django.types import DjangoObjectType
from apps.course.constant import (
    ADVANCE,
    BEGINNER,
    INTERMEDIATE,
)
from apps.course.models import (
    Courses,
    StudentCourse,
)


class CoursesType(DjangoObjectType):
    class Meta:
        model = Courses
        fields = '__all__'


class StudentCourseType(DjangoObjectType):
    class Meta:
        model = StudentCourse
        fields = '__all__'


class Query(graphene.ObjectType):
    schedule_recommendation = graphene.List(
        CoursesType,
        student_id=graphene.Int(required=True)
    )
    course_recommendation = graphene.List(
        CoursesType,
        student_id=graphene.Int(required=True)
    )

    def resolve_schedule_recommendation(self, info, student_id):
        user = info.context.user
        if user.is_anonymous or user.student_id != student_id:
            raise Exception('Authentication required or not Logged in')
        student = MorshedStudent.objects.get(student_id=student_id)
        student_courses = StudentCourse.objects.filter(
            student_id=student
        )
        course_ids = [student_course.course_id.id for student_course in student_courses]
        courses = Courses.objects.filter(
            id__in=course_ids,
            is_external=False
        )

        return courses

    def resolve_course_recommendation(self, info, student_id):
        user = info.context.user
        if user.is_anonymous or user.student_id != student_id:
            raise Exception('Authentication required or not Logged in')
        student = MorshedStudent.objects.get(student_id=student_id)
        level = ''
        if student.student_gpa:
            if student.student_gpa >= 85:
                level = ADVANCE
            elif 75 <= student.student_gpa < 85:
                level = INTERMEDIATE
            else:
                level = BEGINNER
        student_courses = StudentCourse.objects.filter(
            student_id=student
        )
        course_ids = [student_course.course_id.id for student_course in student_courses]
        courses = Courses.objects.filter(
            id__in=course_ids,
            is_external=True,
            course_level=level
        )
        return courses
