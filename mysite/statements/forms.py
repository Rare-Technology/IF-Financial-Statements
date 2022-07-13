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

class EmailForm(forms.Form):
    attach_PDF = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        initial = True
    )
    include_Income_Statement = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        initial = True,
        required = False
    )
    include_Cashflow_Statement = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        initial = True,
        required = False
    )
    to_email = forms.EmailField(
        widget = forms.EmailInput(attrs = {"class": "form-control"}),
        required = True
    )
    subject = forms.CharField(
        widget = forms.TextInput(attrs = {"class": "form-control"}),
        required = True
    )
    body = forms.CharField(
        widget = forms.Textarea(attrs = {"class": "form-control", "rows": "5"}),
        required = True
    )
