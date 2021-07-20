from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login
from libs.utils.paystack_api import PaystackAccount
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from project.models import Plans, Subscription, User
from .forms import UserRegistrationForm
from project.tasks import send_installation_fee_paid_mail
from wash.tokens import account_activation_token

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
			user = form.save(commit=True)
			# prepare email confirmation message
			current_site = get_current_site(request)
			subject = 'Activate Your WaterServer Account'
			message = render_to_string('emails/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject, message)
			messages.success(request, "Account created successfully, Kindly verify your email address before you can login!.")
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


def activate_account_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return HttpResponse('Activation link is invalid')
