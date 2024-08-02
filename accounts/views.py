from django.shortcuts import render

# Create your views here.

def user_registration_view(request):
    return render(request, 'account/register.html')