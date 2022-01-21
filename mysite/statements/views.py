from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "post":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            messages.success(request, "Registratin successful. Hello %s!" % username)
            return redirect('home')
    else:
        form = UserCreationForm()
        ctx = {'form': form}
    return render(request, 'registration/register.html', ctx)

def settings(request):
    return render(request, 'mysite/settings.html')

def home(request):
    return render(request, 'mysite/home.html')
