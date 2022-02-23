from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from ourfish.models import AuthUser
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from mysite.settings import EMAIL_HOST_USER
from xhtml2pdf import pisa
from tempfile import TemporaryFile
from .forms import UpdateAccountForm
import csv
import pandas as pd
from datetime import date
from statements.utils import generate_income_statement, generate_cashflow_statement





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
            messages.error(request, "Error logging in. Please try again.")
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
        ctx = {'income_table': None}
        return render(request, 'mysite/home.html')
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
            'income_table': income_table
        }

        return HttpResponse(income_table)

def export_pdf(request):
    template_path = 'mysite/export_pdf.html'

    user = request.user
    start_date = date.fromisoformat("2022-01-01")#request.POST.get('start-date'))
    end_date = date.fromisoformat("2022-02-22") #request.POST.get('end-date'))
    income = generate_income_statement(user, start_date, end_date)
    # cashflow_statement = generate_cashflow_statement(user, start_date, end_date, income_statement)

    income_table = income.to_html(classes = "table table-striped table-responsive", justify='center')

    context = {'income_statement': income_table}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(
        content_type = 'application/pdf',
        headers = {'Content-Disposition': 'attachment; filename="statement.pdf"'},
    )

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest = response)

    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('Error exporting pdf <pre>' + html + '</pre>')

    return response

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="statement.csv"'},
    )

    writer = csv.writer(response)

    writer.writerow(['Date', 'Fisher', 'Total price'])



    for catch in Catches.objects.all()[:10]:
        writer.writerow([catch.date, catch.fisher_id, catch.total_price])

    return response

def send_email(request):
    if request.method == "POST":
        # create and send Email

        email = EmailMessage(
            "Ourfish Financial Statement",
            "Here is your financial statement for the period from ... to ...",
            EMAIL_HOST_USER,
            [request.user.email]
        )

        # The conditionals on the next if statements look a bit weird but I prefered
        # to write it this way rather than checking the value of eg request.POST['attach_pdf'].
        # Without using a sneaky/hack-y trick, unchecked boxes from the form will not pass in POST
        # and thus will raise a key value error if using request.POST['<key>'] in a conditional
        # see this for the sneaky trick in reference https://stackoverflow.com/questions/1809494/post-unchecked-html-checkboxes
        if 'attach_pdf' in request.POST.keys():
            context = {'data': Catches.objects.all()[:10]}
            template = get_template('mysite/export_pdf.html')
            html = template.render(context)

            pdf_file = TemporaryFile()

            pisa_status = pisa.CreatePDF(html, dest = pdf_file)

            if pisa_status.err:
                return HttpResponse("Something went wrong. Please try again.")

            pdf_file.seek(0)
            email.attach('statement.pdf', pdf_file.read(), 'application/pdf')

            pdf_file.close()

        if 'attach_excel' in request.POST.keys():
            excel_file = TemporaryFile(mode = 'w+')

            writer = csv.writer(excel_file)

            writer.writerow(['Date', 'Fisher', 'Total price']) # Don't forget to change this when changing data !

            data = Catches.objects.all()[:10]
            for row in data:
                writer.writerow([row.date, row.fisher_id, row.total_price])

            excel_file.seek(0)
            email.attach('statement.csv', excel_file.read(), 'text/csv')

            excel_file.close()

        email.send(fail_silently = False)

        messages.success(request, "Your email has been sent. Check your inbox shortly.")
        return redirect("home")

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
