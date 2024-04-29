import graphene
import graphql_jwt
from graphql_jwt import shortcuts
from django.contrib.auth.hashers import check_password
from apps.user_auth.authentication import MorshedStudentIdAuthenticationBackend
from graphene_django import DjangoObjectType
from graphql_auth import mutations
import random
from apps.user_auth.models import (
    OTP,
    MorshedStudent
)


class MorshedStudentType(DjangoObjectType):
    class Meta:
        model = MorshedStudent
        fields = '__all__'


class OTPType(DjangoObjectType):
    class Meta:
        model = OTP
        fields = "__all__"


class ObtainJSONWebToken(graphene.Mutation):
    token = graphene.String()
    refresh_token = graphene.String()
    user = graphene.Field(MorshedStudentType)

    class Arguments:
        student_id = graphene.Int(required=True)

    def mutate(self, info, student_id):
        user = MorshedStudent.objects.get(student_id=student_id)
        if user is None:
            raise Exception('Authentication failed.')
        token = shortcuts.get_token(user)
        refresh_token = shortcuts.create_refresh_token(user.morshed_user)
        return ObtainJSONWebToken(token=token, refresh_token=refresh_token, user=user)


class GenerateOTP(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, student_id):
        morshed_student = MorshedStudent.objects.get(student_id=student_id)
        otp = '{:06d}'.format(random.randint(0, 999999))
        OTP.objects.create(
            user=morshed_student.morshed_user,
            otp_code=otp
        )
        return GenerateOTP(
            success=True,
            message='OTP generated successfully'
        )


class VerifyOTP(graphene.Mutation):
    class Arguments:
        student_id = graphene.Int(required=True)
        otp = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, student_id, otp):
        try:
            morshed_student = MorshedStudent.objects.get(student_id=student_id)
            auth_process = OTP.objects.filter(user_id=morshed_student.morshed_user).latest('created_at')
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
    token_auth = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


class Query(graphene.ObjectType):
    morshed_student = graphene.Field(
        MorshedStudentType,
        student_id=graphene.Int(required=True),
        password=graphene.String(required=True)
    )
    auth_process = graphene.Field(
        OTPType,
        student_id=graphene.Int(required=True)
    )

    def resolve_morshed_student(self, info, student_id, password):
        morshed_student = MorshedStudent.objects.get(student_id=student_id)

        # Check if the provided password matches the user's password
        if not check_password(password, morshed_student.morshed_user.password):
            raise Exception('Invalid password')

        return morshed_student

    def resolve_auth_process(self, info, student_id):
        if not info.context.user.is_authenticated:
            raise Exception('Authentication required.')
        morshed_student = MorshedStudent.objects.get(student_id=student_id)
        return OTP.objects.filter(user_id=morshed_student.morshed_user.id).latest('created_at')
