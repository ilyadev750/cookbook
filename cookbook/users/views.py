from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm

# Create your views here.
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("my_recepies", request.user.username)
        else:
            form = AuthenticationForm()
            context = {"form": form, "error": 'Invalid login or password, try again!'}
            return render(request, "users/login.html", context)
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form, "error": ''})

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("my_recepies", request.user.username)
    else:
        form = CustomUserCreationForm()
    return render(request, "users/registration.html", {"form": form})

def logout_user(request):
    logout(request)
    return redirect("home")