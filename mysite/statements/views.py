from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.utils.translation import get_language, activate, gettext as _
from ourfish.models import AuthUser, FishdataBuyer
from mysite.settings import EMAIL_HOST_USER
from xhtml2pdf import pisa
from tempfile import TemporaryFile
from .forms import UpdateAccountForm, EmailForm
import csv
import pandas as pd
from datetime import date
from statements.utils import generate_income_statement, generate_cashflow_statement, format_data, get_currency, translate_date, month_translations
import json
import numpy as np
import base64

# Create your views here.
def loginAccount(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, _("Error logging in. Please try again."))
            return redirect('login')
    else:
        return render(request, 'registration/login.html', {})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please follow the directions below and try again.")
    else:
        form = UserCreationForm()
    ctx = {'form': form}
    return render(request, 'registration/register.html', ctx)

def updateAccount(request):
    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            messages.info(request, "Your email address has been updated.")
            return redirect('home')
        else:
            messages.error(request, "Could not change information. Please try again.")
    else:
        form = UpdateAccountForm(instance = request.user)
    ctx = {'form': form}
    return render(request, 'registration/update.html', ctx)

def changePassword(request):
    if request.method == "POST":

        form = PasswordChangeForm(user = request.user, data = request.POST)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('home')
        else:
            messages.success(request, "Could not change password. Double check the instructions and try again.")
    else:
        form = PasswordChangeForm(user = request.user)
    ctx = {'form': form}
    return render(request, 'registration/password.html', ctx)

def deleteAccount(request):
    return render(request, 'mysite/delete.html')

def home(request):
    if request.user.is_authenticated:
        user = request.user
        of_user = AuthUser.objects.get(username = user.username)
        buyer = FishdataBuyer.objects.get(user = of_user)

        income = generate_income_statement(buyer)
        cashflow = generate_cashflow_statement(buyer, income)

        income.index = income.index.map(lambda x: x.strftime('%b %Y'))
        cashflow.index = cashflow.index.map(lambda x: x.strftime('%b %Y'))

        income_table = [
            {
                'metric': name.split('_')[0],
                'source': name.split('_')[1],
                'data': col.apply(lambda x: format_data(buyer, x)).values
            } for name, col in income.items()
        ]
        income_dates = income.reset_index()['date'].map(lambda x: translate_date(x)).values

        cashflow_table = [
            {
                'metric': name,
                'data': col.apply(lambda x: format_data(buyer, x)).values
            } for name, col in cashflow.items()
        ]
        cashflow_dates = cashflow.index.map(lambda x: translate_date(x)).values
        currency = get_currency(buyer)

        income = income.reset_index()
        income = income.rename({
            'Net income_Total': _('Net income')
        }, axis = 1)
        income_json = income.to_json(orient = 'records')

        ### make 0 line very visible !! black/emphasize 0
        cashflow = cashflow.reset_index()
        cashflow = cashflow.rename({
            'Total cash from fisheries operations': _('Total cash from fisheries operations')
        }, axis = 1)
        cashflow_json = cashflow.to_json(orient = 'records')

        help = {
            _('Revenue'): _("Revenue is the money that is generated by the sale of fish or supplies."),
            _('Expenses'): _("Expense is the money you need to pay for the fish or supplies you use or buy."),
            _('Profit (Loss)'): _("If revenue is greater than expenses during the same period of time, a profit is made. If expenses are greater than revenue during the same period of time, a loss is made."),
            _('Net income'): _("Net income is calculated by subtracting all expenses from all revenues during the same period of time. If the resulting balance is positive, an accounting profit is made; if the resulting balance is negative, an accounting loss is made.")
        }

        ctx = {
            'income_table': income_table,
            'income_dates': income_dates,
            'income_json': income_json,
            'net_income': _('Net income'),
            'cashflow_table': cashflow_table,
            'cashflow_dates': cashflow_dates,
            'cashflow_json': cashflow_json,
            'total_cash': _('Total cash from fisheries operations'),
            'currency': currency,
            'help': help
        }

        request.session['income_json'] = income_json
        request.session['cashflow_json'] = cashflow_json
        request.session['currency'] = currency

        ### For offline (not on Postgres server whitelist) testing only
        # with open('ctx.json', 'r', encoding='UTF-8') as f:
        #     ctx = json.load(f)

        return render(request, 'mysite/home.html', ctx)
    else:
        return redirect('login')

def view_statement(request):
    if request.method == "POST":
        user = request.user
        start_date = date.fromisoformat("2022-01-01")#request.POST.get('start-date'))
        end_date = date.fromisoformat("2022-02-22") #request.POST.get('end-date'))
        income = generate_income_statement(user, start_date, end_date)
        # cashflow_statement = generate_cashflow_statement(user, start_date, end_date, income_statement)

        income_table = income.to_html(classes = "table table-striped table-responsive", justify='left')
        ctx = {
            'income_table': income_table,
            'start_date': start_date,
            'end_date': end_date
        }

        return HttpResponse(income_table)

def send_email(request):
    if request.method == "POST":
        if 'start_date' in request.POST.keys():
            # User was sent from the home page. Set up form and attachments.
            user = request.user
            of_user = AuthUser.objects.get(username = user.username)
            buyer = FishdataBuyer.objects.get(user = of_user)

            income_json = json.loads(request.session['income_json'])
            cashflow_json = json.loads(request.session['cashflow_json'])
            currency = request.session['currency']
            start_date = pd.to_datetime(request.POST['start_date'])
            end_date = pd.to_datetime(request.POST['end_date'])

            # Have to reconstruct income/cashflow dataframes since these cannot be parsed in request.session
            income = pd.json_normalize(income_json)
            income['datetime_date'] = pd.to_datetime(income['date'])
            income = income.query("@start_date <= datetime_date and datetime_date <= @end_date")
            income = income.drop('datetime_date', axis = 1).set_index('date')
            income = income.rename({
                _('Net income'): 'Net income_Total'
            }, axis = 1)

            cashflow = pd.json_normalize(cashflow_json)
            cashflow['datetime_date'] = pd.to_datetime(cashflow['date'])
            cashflow = cashflow.query("@start_date <= datetime_date and datetime_date <= @end_date")
            cashflow = cashflow.drop('datetime_date', axis = 1).set_index('date')
            cashflow = cashflow.rename({
                _('Total cash from fisheries operations'): 'Total cash from fisheries operations'
            }, axis = 1)

            income_table = [
                {
                    'metric': name.split('_')[0],
                    'source': name.split('_')[1],
                    'data': col.apply(lambda x: format_data(buyer, x)).values
                } for name, col in income.items()
            ]
            income_dates = income.reset_index()['date'].map(lambda x: translate_date(x)).values

            cashflow_table = [
                {
                    'metric': name,
                    'data': col.apply(lambda x: format_data(buyer, x)).values
                } for name, col in cashflow.items()
            ]
            cashflow_dates = cashflow.index.map(lambda x: translate_date(x)).values

            source_table = None
            if 'income-submit' in request.POST.keys():
                source_table = 'income'
            elif 'cashflow-submit' in request.POST.keys():
                source_table = 'cashflow'

            form = EmailForm(source_table = source_table)

            ctx = {
                'income_table': income_table,
                'income_dates': income_dates,
                'cashflow_table': cashflow_table,
                'cashflow_dates': cashflow_dates,
                'currency': currency,
                'form': form
            }

            return render(request, 'mysite/send-email.html', ctx)
        else:
            # User submitted a POST request w/ email info. Create and send Email
            form = EmailForm(request.POST, source_table = None)
            if form.is_valid():
                recipients = request.POST['to_email'].split(',')
                for r in recipients:
                    r = r.strip()

                email = EmailMessage(
                    subject = request.POST['subject'],
                    body = request.POST['body'],
                    from_email = EMAIL_HOST_USER,
                    bcc = recipients
                )

                user_name = request.user.first_name
                if 'include_Income_Statement' in request.POST.keys():
                    income_pdf_decode = base64.b64decode(request.POST['income_pdf_raw'])
                    email.attach(user_name + '_Income_Statement.pdf', income_pdf_decode, 'application/pdf')

                    ### For offline use
                    # email.body = '===== INCOME STATEMENT =====\n\n' + email.body

                if 'include_Cash_Flow_Statement' in request.POST.keys():
                    cashflow_pdf_decode = base64.b64decode(request.POST['cashflow_pdf_raw'])
                    email.attach(user_name + '_Cash Flow_Statement.pdf', cashflow_pdf_decode, 'application/pdf')

                    ### For offline use
                    # email.body = '===== CASHFLOW STATEMENT =====\n\n' + email.body

                email.send(fail_silently = False)

                messages.success(request, _("Your email has been sent."))
                return redirect('/')
    else:
        return HttpResponse("Please click the Send Email button on the home page.<br><a href='/'>Return home</a>")

def print_statement(request):
    user = request.user
    start_date = date.fromisoformat("2022-01-01")#request.POST.get('start-date'))
    end_date = date.fromisoformat("2022-02-22") #request.POST.get('end-date'))
    income = generate_income_statement(user, start_date, end_date)
    # cashflow_statement = generate_cashflow_statement(user, start_date, end_date, income_statement)

    income_table = income.to_html(classes = "table table-striped table-responsive", justify='center')
    ctx = {
        'income_statement': income_table
    }

    return render(request, 'mysite/print_statement.html', ctx)
