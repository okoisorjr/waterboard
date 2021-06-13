from django.conf import settings
from libs.utils.paystack_api import PaystackAccount
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from project.models import Plans
from .forms import UserRegistrationForm

# Create your views here.
def index(request):
	return render(request, 'project/index.html')

@login_required
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


@login_required
def subscribe(request):
	plan = None
	user_type = None
	if request.user.is_organization:
		plan = Plans.objects.filter(name__icontains='org').first()
		user_type = "Organization"
	else:
		plan = Plans.objects.filter(name__icontains='ind').first()
		user_type = "Residential"

	paystack = PaystackAccount(
            email=settings.PAYSTACK_EMAIL,
            public_key=settings.PAYSTACK_PUBLIC_KEY,
            amount= plan.price
        )
	context = dict(
		paystack=paystack,
		plan=plan,
		user_type=user_type
	)
	return render(request, 'project/checkout.html', context=context)