from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# This is the home view for the recipe book application.
# It renders the home.html template when accessed.
def home(request):
    return render(request, "home.html")


# This is the signup view for the recipe book application.
# It handles user registration and automatically logs in the user after successful signup.
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")
            messages.success(
                request, f"Account created for {username}! You can now log in."
            )
            login(request, user)  # Automatically log in after signup
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
