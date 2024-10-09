from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'cabinet/body/index.html')
#
def fiscalite(request):
    return render(request,'cabinet/body/fiscalite.html')
#
def comptabilite(request):
    return render(request,'cabinet/body/comptabilite.html')
#
def juridique(request):
    return render(request,'cabinet/body/juridique.html')
#
def management(request):
    return render(request,'cabinet/body/management.html')
#
def contacts(request):
    return render(request,'cabinet/body/contact.html')
#
#
def blog(request):
    return render(request,'cabinet/body/blog.html')