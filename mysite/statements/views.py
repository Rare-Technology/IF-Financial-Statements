from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage
from mysite.settings import EMAIL_HOST_USER
from xhtml2pdf import pisa
from tempfile import NamedTemporaryFile, TemporaryDirectory
from .models import Catches
from .forms import UpdateAccountForm
import csv

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
            messages.success(request, "Error logging in. Please try again.")
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
            messages.success(request, "Registration failed. Please follow the directions below and try again.")
    else:
        form = UserCreationForm()
    ctx = {'form': form}
    return render(request, 'registration/register.html', ctx)

def updateAccount(request):
    if request.method == "POST":
        form = UpdateAccountForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            messages.success(request, "Could not change information. Please try again.")
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
            messages.success("Could not change password. Double check the instructions and try again.")
    else:
        form = PasswordChangeForm(user = request.user)
    ctx = {'form': form}
    return render(request, 'registration/password.html', ctx)



def deleteAccount(request):
    return render(request, 'mysite/delete.html')

def home(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            # create and send Email

            context = {'Catches': Catches.objects.all()[:10]}
            template = get_template('mysite/export_pdf.html')
            html = template.render(context)

            tmpdir = TemporaryDirectory()
            pdf_file = NamedTemporaryFile(dir = tmpdir)

            pisa_status = pisa.CreatePDF(html, dest = pdf_file)

            if pisa_status.err:
                return HttpResponse("Something went wrong. Please try again.")

            email = EmailMessage(
                "Ourfish Financial Statement",
                "Here is your financial statement for the period from ... to ...",
                EMAIL_HOST_USER,
                request.user.email,
                attachments = [(pdf_file.name, pdf_file, 'application/zip')]
            )
            email.send(fail_silently = False)

            pdf_file.close()
            tmpdir.close()

        table_data = Catches.objects.all()

        ctx = {
            'table_data': table_data
        }

        return render(request, 'mysite/home.html', ctx)
    else:
        return render(request, 'mysite/home.html')

def export_pdf(request):
    template_path = 'mysite/export_pdf.html'
    context = {'Catches': Catches.objects.all()[:10]}

    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')

    # to directly download the pdf we need attachment
    response['Content-Disposition'] = 'attachment; filename="statement.pdf"'

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
