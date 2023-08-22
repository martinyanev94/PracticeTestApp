from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required(login_url='/authentication/login')
# Create your views here.
def home_page_view(request):
    return render(request, 'homepage/home_page.html')
