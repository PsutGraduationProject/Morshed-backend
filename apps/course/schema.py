import json

import graphene
from django.db.models import Q
from apps.user_auth.models import MorshedStudent
from apps.schedule_recommendation_model import recommend_and_predict_grades
from apps.course_recommendation_model import recommend_courses_for_student
from graphene_django.types import DjangoObjectType
from apps.course.constant import (
    ADVANCE,
    BEGINNER,
    INTERMEDIATE,
    ALL
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

        course_numbers = schedule_recommendation.keys()
        course_numbers = list(map(int, course_numbers))
        courses = Courses.objects.filter(
            course_number__in=course_numbers,
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
        course_recommendation = recommend_courses_for_student(student_id)
        course_numbers = [course_number for course_number in course_recommendation.keys()]
        courses = Courses.objects.filter(
            course_number__in=course_numbers,
            is_external=True
        )
        for course in courses:
            course.course_price = course_recommendation[course.course_number]['price']
            course.course_provider = 'Udemy'
            if "All Levels" in course_recommendation[course.course_number]['level']:
                course.course_level = ALL
            elif "Beginner Level" in course_recommendation[course.course_number]['level']:
                course.course_level = BEGINNER
            elif "Intermediate Level" in course_recommendation[course.course_number]['level']:
                course.course_level = INTERMEDIATE
            elif "Expert Level" in course_recommendation[course.course_number]['level']:
                course.course_level = ADVANCE
            course.number_of_hours = course_recommendation[course.course_number]['content_duration']
            course.course_url = course_recommendation[course.course_number]['url']
            course.course_image = course_recommendation[course.course_number]['course_image']
            course.course_image_detail = course_recommendation[course.course_number]['course_image']
        Courses.objects.bulk_update(
            courses,
            ['course_price', 'course_provider', 'course_level', 'number_of_hours', 'course_url', 'course_image',
             'course_image_detail']
        )
        return courses
