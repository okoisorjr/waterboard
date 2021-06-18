from wash.celery import app
from wash.tasks import send_email
from .models import User



@app.task
def send_installation_fee_paid_mail(user_id):

    user = User.objects.get(id=user_id)
    # user.paid_installment_fee = True
    # user.save()
    subject = f"PAYMENT FOR INSTALLATION SUCCESSFUL"
    return send_email(
        subject=subject, to_email=[user.email],
        email_template='installation_mail.html',
        username=user.username
    )