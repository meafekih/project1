# For pruposes of this article I have ommitted a number of stuff in this snippet
# to only the most relevant

from .forms import forms
from .models import Company

class CreateCompanyMutationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name",
            "logo",
        ]