import graphene
from apps.course.schema import Query as CourseQuery
from apps.user_auth.schema import (
    OTPMutation,
    AuthMutation,
    Query as UserQuery
)


class Query(UserQuery, CourseQuery, graphene.ObjectType):
    pass


class Mutation(OTPMutation, AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
