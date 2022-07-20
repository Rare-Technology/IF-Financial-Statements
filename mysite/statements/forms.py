from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


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

class MultiEmailField(forms.CharField):
    widget = forms.EmailInput
    default_validators = [validators.validate_email]

    def __init__(self, **kwargs):
        super().__init__(strip = True, **kwargs)

    def run_validators(self, value):
        if value in self.empty_values:
            return
        errors = []
        for v in self.validators:
            try:
                for val in value.split(','):
                    val = val.strip()
                    v(val)
            except ValidationError as e:
                if hasattr(e, "code") and e.code in self.error_messages:
                    e.message = self.error_messages[e.code]
                errors.extend(e.error_list)
        if errors:
            raise ValidationError(errors)

class EmailForm(forms.Form):
    def __init__(self, *args, **kwargs):
        source_table = kwargs.pop('source_table')
        super().__init__(*args, **kwargs)

        self.source_table = source_table
        self.fields['include_Income_Statement'].initial = True if self.source_table == 'income' else False
        self.fields['include_Cashflow_Statement'].initial = True if self.source_table == 'cashflow' else False

    attach_PDF = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        initial = True
    )
    include_Income_Statement = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        required = False
    )
    include_Cashflow_Statement = forms.BooleanField(
        widget = forms.CheckboxInput(attrs = {"class": "form-check-input"}),
        required = False
    )
    to_email = MultiEmailField(
        widget = forms.EmailInput(attrs = {
            "class": "form-control",
            "multiple": "",
            "placeholder": "loans@bank1.com,loans@bank2.com"
        }),
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
