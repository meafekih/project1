

# For pruposes of this article I have ommitted a number of stuff in this snippet
# to only the most relevant

import graphene
from graphql.execution.base import ResolveInfo
from graphql_auth.bases import Output
from graphene_file_upload.scalars import Upload

from .forms import CreateCompanyMutationForm

class CreateCompanyMutation(graphene.Mutation, Output):
    form = CreateCompanyMutationForm

    class Arguments:
        """Necessary input to create a new Company."""
        name = graphene.String(required=True, description="Company name")
        logo = Upload(required=False, description="Logo for the Company.",)

    def mutate(self, info: ResolveInfo, logo=None, **data) -> "CreateCompanyMutation":
        """Mutate method."""
        file_data = {}
        if logo:
            file_data = {"logo": logo}

        # https://docs.djangoproject.com/en/3.2/ref/forms/api/#binding-uploaded-files-to-a-form
        # Binding file data to the Form.
        f = CreateCompanyMutation.form(data, file_data)

        if f.is_valid():
            f.save()
            return CreateCompanyMutation(success=True)
        else:
            return CreateCompanyMutation(
                success=False, errors=f.errors.get_json_data()
            )