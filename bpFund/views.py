from django.shortcuts import render
from django.http import HttpResponse

# from .models import Causes

# Create your views here.

#function extends from index.html, which contains navbar, but renders home. donate.html and starp.html templates extend index.html
def index(request):
    return render(request, "bpFund/home.html")

def donate(request):
    causes = 0 #Causes.objects.get()
    return render(request, "bpFund/donate.html", {
        causes: causes,
    })

def starp(request):
    return render(request, "bpFund/starp.html")

def createProject(request):
    if request.method == "POST":
        print("here")
        name = request.POST["name"]
        email = request.POST["emailForm"]
        orgSchool = request.POST["org"]
        location = request.POST["location"]
        date = request.POST["date"]
        targetAmount = request.POST["tarAmount"]

        print("here", name, email, orgSchool, location, date, targetAmount)
        return redner(request, 'bpFund/starp.html', {
            message: "Submitted!"
        })
    return HttpResponse("None")
