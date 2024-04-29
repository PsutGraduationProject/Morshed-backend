from apps.user_auth.models import MorshedStudent
from graphql_jwt.backends import JSONWebTokenBackend
from graphql_jwt.exceptions import JSONWebTokenError


class MorshedStudentIdAuthenticationBackend(JSONWebTokenBackend):
    def authenticate(self, request=None, **credentials):
        student_id = credentials.get('student_id')

        if student_id is None:
            return None

        try:
            user = MorshedStudent.objects.get(student_id=student_id)
        except MorshedStudent.DoesNotExist:
            raise JSONWebTokenError('Student with this ID does not exist')

        return user


