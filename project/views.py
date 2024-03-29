from django.conf import settings
from django.contrib import messages
from libs.utils.paystack_api import PaystackAccount
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from project.models import Plans, Subscription, User
from .forms import UserRegistrationForm
from project.tasks import send_installation_fee_paid_mail



# Create your views here.
def index(request):
	return render(request, 'project/index.html')

@login_required
def dashboard(request):
	if request.user.is_superuser:
		return redirect('/admin')
	return render(request, 'project/dashboard.html')

def register(request):
	form = UserRegistrationForm()
	if request.method == "POST":
		form =  UserRegistrationForm(request.POST or None)
		if form.is_valid():
			form.save(commit=True)
		messages.success(request, "Account created successfully, Please Login!.")
		return redirect(reverse('login'))
	context = dict(form=form)
	return render(request, 'registration/register.html', context=context)


@login_required
def subscribe(request):
	# only verifed and people who have paid installation fee can access
	if not (request.user.verified and request.user.paid_installment_fee):
		messages.info(
			request, "Only users whose addresses have been verified and have paid their installation fee can access this page!."
			)
		return redirect(reverse('dashboard'))
	plan = None
	user_type = None
	if request.user.is_organization:
		plan = Plans.objects.filter(name__icontains='org').first()
		user_type = "Commercial"
	else:
		plan = Plans.objects.filter(name__icontains='ind').first()
		user_type = "Residential"
	paystack = PaystackAccount(
            email=request.user.email,
            public_key=settings.PAYSTACK_PUBLIC_KEY,
            amount= plan.price
        )
	if request.method == "POST":
		if paystack.verify_transaction(request.POST['reference']):
			user_sub, _ = Subscription.objects.get_or_create(user=request.user)
			# print(user_sub)
			user_sub.activate_subscription(plan)
			messages.success(request, "Payment was successful. Your subscription has been activated!.")
			return redirect(reverse('dashboard'))
		else:
			messages.error(request, "Payment Not successful, Please try again")
			return redirect(reverse('dashboard'))
	context = dict(
		paystack=paystack,
		plan=plan,
		user_type=user_type
	)
	return render(request, 'project/checkout.html', context=context)


@login_required
def pay_installation_fee(request):

	if not request.user.paid_installment_fee is False:
		messages.info(
			request, "Installation fee already paid!."
			)
		return redirect(reverse('dashboard'))
	amount = None
	user_type = None
	if request.user.is_organization:
		amount = 50000.00
		user_type = "Commercial"
	else:
		amount = 10000.00
		user_type = "Residential"
	paystack = PaystackAccount(
            email=request.user.email,
            public_key=settings.PAYSTACK_PUBLIC_KEY,
            amount= amount
        )
	if request.method == "POST":
		if paystack.verify_transaction(request.POST['reference']):
			user = User.objects.get(id=request.user.id)
			send_installation_fee_paid_mail.delay(user.id)
			messages.success(request, "Payment was successful!.")
			return redirect(reverse('dashboard'))
		else:
			messages.error(request, "Payment Not successful, Please try again")
			return redirect(reverse('dashboard'))
	context = dict(
		paystack=paystack,
		amount = amount,
		user_type = user_type
	)
	return render(request, 'project/installation.html', context=context)