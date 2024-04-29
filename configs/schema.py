import graphene
from apps.user_auth.schema import (
    OTPMutation,
    AuthMutation,
    Query as UserQuery
)


class Query(UserQuery, graphene.ObjectType):
    pass


class Mutation(OTPMutation, AuthMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)
