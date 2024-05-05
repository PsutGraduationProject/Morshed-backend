import graphene
import graphql_jwt
from graphql_jwt import shortcuts
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from graphene_django import DjangoObjectType
from graphql_auth import mutations
import random
from apps.user_auth.models import (
    OTP,
    MorshedStudent,
)


class MorshedStudentType(DjangoObjectType):
    class Meta:
        model = MorshedStudent
        fields = '__all__'


class OTPType(DjangoObjectType):
    class Meta:
        model = OTP
        fields = "__all__"


class GenerateOTP(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    otp = graphene.Int()

    def mutate(self, info):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception('Authentication required or Wrong student ID provided')

        morshed_student = MorshedStudent.objects.get(student_id=user.student_id)

        if morshed_student is None:
            raise Exception('Invalid User')

        otp = '{:06d}'.format(random.randint(0, 999999))
        OTP.objects.create(
            morshed_user=morshed_student,
            otp_code=otp
        )
        return GenerateOTP(
            success=True,
            message="OTP generated successfully",
            otp=otp
        )


class VerifyOTP(graphene.Mutation):
    class Arguments:
        otp = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, otp):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication required or invalid credentials.')
        try:
            morshed_student = MorshedStudent.objects.get(student_id=user.student_id)
            auth_process = OTP.objects.filter(morshed_user=morshed_student).latest('created_at')
            if auth_process.is_otp_valid(otp):
                return VerifyOTP(success=True, message="OTP verified successfully.")
            else:
                return VerifyOTP(success=False, message="Invalid or expired OTP.")
        except OTP.DoesNotExist:
            return VerifyOTP(success=False, message="No OTP record found.")
        except MorshedStudent.DoesNotExist:
            return VerifyOTP(success=False, message="No student record found.")

class OTPMutation(graphene.ObjectType):
    generate_otp = GenerateOTP.Field()
    verify_otp = VerifyOTP.Field()


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    morshed_student = graphene.Field(
        MorshedStudentType,
        student_id=graphene.Int(required=True),
        password=graphene.String(required=True)
    )

    def resolve_morshed_student(self, info, student_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication required or invalid credentials.')

        morshed_student = get_object_or_404(
            MorshedStudent,
            student_id=student_id
        )

        return morshed_student
