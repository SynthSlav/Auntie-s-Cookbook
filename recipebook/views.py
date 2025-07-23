from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages


# This is the home view for the recipe book application.
# It renders the home.html template when accessed.
def home(request):
    """This view renders the home page of the recipe book application."""
    return render(request, "home.html")


# This is the signup view for the recipe book application.
# It handles user registration and automatically logs in the user after successful signup.
def signup_view(request):
    """This view handles user signup. It uses Django's built-in UserCreationForm to create a new user.
    If the form is valid, it saves the user and logs them in automatically."""
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


def login_required_message(request):
    """This view handles the case where a user tries to access a feature that requires login.
    It displays a warning message and redirects the user to the login page."""
    feature = request.GET.get("feature", "this feature")
    # Display a warning message if the user is not logged in
    messages.warning(
        request,
        f"You need to be logged in to {feature}. Please log in or sign up.",
    )
    referer = request.META.get("HTTP_REFERER", "/")  # Get the referring URL
    return redirect(referer)  # Redirect to the referring page
