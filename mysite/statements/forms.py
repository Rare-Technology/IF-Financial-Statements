from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms

class UpdateAccountForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ('email',)
        exclude = ('password',)
    # TODO: add site language as a field

class StatementForm(forms.Form):
    start_date = forms.DateTimeField()
    end_date = forms.DateTimeField()
