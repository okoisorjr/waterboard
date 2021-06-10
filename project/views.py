from django.shortcuts import render

# Create your views here.

def index(request):
	return render(request, 'project/index.html')

def dashboard(request):
	return render(request, 'project/dashboard.html')

def subscription(request):
	return render(request, 'project/subscription.html')
	

	
