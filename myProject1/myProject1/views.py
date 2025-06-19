#from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    #return HttpResponse("Welcome to myProject1 home page! 😍🎉🎉🎈This is the main entry point of the application.")
    return render(request, 'home.html')

def about(request):
    #return HttpResponse("This is the about page of myProject1. Here you can find information about the project and its purpose. 🎉🎈")
    return render(request, 'about.html')