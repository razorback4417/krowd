from django.shortcuts import render
from django.http import HttpResponse

from django.conf import settings
from .models import Cause

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
        print("In createProject() POST method.")
        name = request.POST["name"]
        email = request.POST["emailForm"]
        orgSchool = request.POST["org"]
        problem = request.POST["prob"]
        sol = request.POST["sol"]
        location = request.POST["location"]
        date = request.POST["date"]
        targetAmount = request.POST["targetAmount"]

        causeModel = Cause(
            name=name,
            email=email,
            orgSchool=orgSchool,
            problem=problem,
            sol=sol,
            location=location,
            date=date,
            targetAmount=targetAmount
        )

        causeModel.save()

        causes = Cause.objects.all()

        #products = Products.objects.all()
        #userstamp = request.user
        #user_rec = User.objects.get(username=userstamp)
        #Tutor.objects.all().filter(active='Y').order_by('subject')
        print("CAUSE MODEL: ", causes)

        return render(request, 'bpFund/donate.html', {
            causes: causes,
        })
    return HttpResponse("None")
