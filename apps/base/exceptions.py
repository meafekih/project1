from django.utils.translation import gettext as _
from graphql import GraphQLError

class GraphQLAuthError(GraphQLError):
    default_message = None
    def __init__(self, message=None):
        if message is None:
            message = self.default_message
        super().__init__(message)


class EMAIL_DUPLICATE(GraphQLAuthError):
    default_message = _("Email duplicate")

class AUTHENTICATION_REQUIRED(GraphQLAuthError):
    default_message = _("Autentication required")

class UNAUTHORIZED(GraphQLAuthError):
    default_message = _("You are not Authorized!")
