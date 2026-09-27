from django.shortcuts import render
from django.http import HttpResponse

def nosotros(request):
    return render(request,'nosotros/index.html')

