from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UpdateAccountForm(UserChangeForm):
    password = None
    
    class Meta:
        model = User
        fields = ('email',)
        exclude = ('password',)
    # TODO: add site language as a field
