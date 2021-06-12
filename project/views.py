from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.

def index(request):
	return render(request, 'project/index.html')

def dashboard(request):
	if request.user.is_superuser:
		return redirect('/admin')
	return render(request, 'project/dashboard.html')

def plans(request):
	return render(request, 'project/subscription.html')
	
