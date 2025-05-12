#from django.http import HttpResponse
from django.shortcuts import render

def homepage (request):
    #return HttpResponse("HELLO FROM HOME PAGE!!!")
    return render(request,'home.html')
def about (request):
    #return HttpResponse("HELLO FROM ABOUT PAGE!!!")
    return render(request,'about.html')
