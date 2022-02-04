from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Catches

# Create your views here.
def loginAccount(request):
    print("HELLO")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, "Error logging in. Please try again.")
            print("did not log in")
            return redirect('login')
    else:
        print("not post?")
        return render(request, 'registration/login.html', {})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request, "Registration successful. Hello %s!" % username)
            return redirect('home')
    else:
        form = UserCreationForm()
        ctx = {'form': form}
        return render(request, 'registration/register.html', ctx)

def updateAccount(request):
    return render(request, 'mysite/update.html')

def deleteAccount(request):
    return render(request, 'mysite/delete.html')

def home(request):
    table_data = Catches.objects.all()

    ctx = {
        'table_data': table_data
    }

    return render(request, 'mysite/home.html', ctx)
