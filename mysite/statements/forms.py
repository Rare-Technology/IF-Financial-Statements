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

class EmailForm(forms.Form):
    attach_PDF = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        initial = True,
        localize = True
    )
    Recipient = forms.EmailField(
        widget = forms.EmailInput(attrs = {"class": "form-control"}),
        required = True,
        localize = True
    )
    subject = forms.CharField(
        widget = forms.TextInput(attrs = {"class": "form-control"}),
        required = True,
        localize = True
    )
    body = forms.CharField(
        widget = forms.Textarea(attrs = {"class": "form-control", "rows": "5"}),
        required = True,
        initial = "Hello world!",
        localize = True
    )
