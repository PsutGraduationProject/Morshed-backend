import graphene
from graphql_auth import relay


class AuthMutation(graphene.ObjectType):
    # graphql_auth mutations
    register = relay.Register.Field()
    verify_account = relay.VerifyAccount.Field()
    update_account = relay.UpdateAccount.Field()
    resend_activation_email = relay.ResendActivationEmail.Field()
    delete_account = relay.DeleteAccount.Field()

    # JWT mutations
    token_auth = relay.ObtainJSONWebToken.Field()
    verify_token = relay.VerifyToken.Field()
    refresh_token = relay.RefreshToken.Field()
    revoke_token = relay.RevokeToken.Field()
