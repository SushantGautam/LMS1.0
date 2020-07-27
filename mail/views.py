from django.shortcuts import render

# Create your views here.
def MailList(request):
    return render(request, 'mail/index.html')