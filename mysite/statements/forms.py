from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

class UpdateAccountForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'password')
