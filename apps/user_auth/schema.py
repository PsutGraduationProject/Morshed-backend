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
    """
    MorshedStudentType class is used to define the type of the MorshedStudent model
    """
    class Meta:
        """
        Metaclass is used to define the model and fields of the MorshedStudentType
        """
        model = MorshedStudent
        fields = '__all__'


class OTPType(DjangoObjectType):
    """
    OTPType class is used to define the type of the OTP model
    """
    class Meta:
        """
        Metaclass is used to define the model and fields of the OTPType
        """
        model = OTP
        fields = "__all__"


class GenerateOTP(graphene.Mutation):
    """
    GenerateOTP class is used to generate OTP for the user
    """
    success = graphene.Boolean()
    message = graphene.String()
    otp = graphene.Int()

    def mutate(self, info):
        """
        mutate method is used to generate OTP for the user
        """
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
    """
    VerifyOTP class is used to verify the OTP for the user
    """
    class Arguments:
        """
        Arguments class is used to define the arguments of the VerifyOTP class
        """
        otp = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, otp):
        """
        mutate method is used to verify the OTP for the user
        """
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
    """
    OTPMutation class is used to define the OTP mutations of the user
    """
    generate_otp = GenerateOTP.Field()
    verify_otp = VerifyOTP.Field()


class AuthMutation(graphene.ObjectType):
    """
    AuthMutation class is used to define the authentication mutations of the user
    """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    """
    Query class is used to define the queries of the MorshedStudentType
    """
    morshed_student = graphene.Field(
        MorshedStudentType,
        student_id=graphene.Int(required=True),
    )

    def resolve_morshed_student(self, info, student_id):
        """
        resolve_morshed_student method is used to get the MorshedStudent
        """
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Authentication required or invalid credentials.')

        morshed_student = get_object_or_404(
            MorshedStudent,
            student_id=student_id
        )

        return morshed_student
