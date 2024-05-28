import graphene
from django.db.models import Q
from apps.user_auth.models import MorshedStudent
from apps.schedule_recommendation_model import recommend_and_predict_grades
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
    """
    CoursesType class is used to define the type of the Courses model
    """
    class Meta:
        """
        Metaclass is used to define the model and fields of the CoursesType
        """
        model = Courses
        fields = '__all__'


class StudentCourseType(DjangoObjectType):
    """
    StudentCourseType class is used to define the type of the StudentCourse model
    """
    class Meta:
        """
        Metaclass is used to define the model and fields of the StudentCourseType
        """
        model = StudentCourse
        fields = '__all__'


class Query(graphene.ObjectType):
    """
    Query class is used to define the queries of the CoursesType
    """
    schedule_recommendation = graphene.List(
        CoursesType,
        student_id=graphene.Int(required=True)
    )
    course_recommendation = graphene.List(
        CoursesType,
        student_id=graphene.Int(required=True)
    )

    def resolve_schedule_recommendation(self, info, student_id):
        """
        resolve_schedule_recommendation method is used to get the schedule recommendation
        """
        user = info.context.user
        if user.is_anonymous or user.student_id != student_id:
            raise Exception('Authentication required or not Logged in')
        schedule_recommendation = recommend_and_predict_grades(student_id)

        course_ids = schedule_recommendation.keys()
        course_ids = list(map(int, course_ids))
        courses = Courses.objects.filter(
            course_number__in=course_ids,
            is_external=False
        )
        for course in courses:
            course.course_grade = schedule_recommendation[str(course.course_number)]
        Courses.objects.bulk_update(courses, ['course_grade'])
        return courses

    def resolve_course_recommendation(self, info, student_id):
        """
        resolve_course_recommendation method is used to get the course recommendation
        """
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
