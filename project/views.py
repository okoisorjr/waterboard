from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import UserRegistrationForm

# Create your views here.

def index(request):
	return render(request, 'project/index.html')

def dashboard(request):
	if request.user.is_superuser:
		return redirect('/admin')
	return render(request, 'project/dashboard.html')

def plans(request):
	return render(request, 'project/subscription.html')
	
def register(request):
	form = UserRegistrationForm()
	if request.method == "POST":
		form =  UserRegistrationForm(request.POST or None)
		if form.is_valid():
			form.save(commit=True)
		return redirect(reverse('login'))
	context = dict(form=form)
	return render(request, 'registration/register.html', context=context)