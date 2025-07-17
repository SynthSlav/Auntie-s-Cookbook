from django.shortcuts import render


# This is the home view for the recipe book application.
# It renders the home.html template when accessed.
def home(request):
    return render(request, "home.html")
