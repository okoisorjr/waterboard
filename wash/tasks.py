"""
    Celery messaging Tasks

    .. warning::
        Read comments in :py:mod:`dhis2.apps.main.tasks` before implementing or changing this code
"""

from __future__ import absolute_import, unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from wash.celery import app

@app.task(bind=True)
def send_email(self,  # pylint: disable=too-many-arguments
               subject,
               email_template,
               instance_id=None,
               to_email=None,
               from_email=settings.DEFAULT_FROM_EMAIL,
               context=None,
               username=None):
    """
    Send asynchronous emails relating to instance.

    :param subject: Subject of the email
    :type subject: string
    :param email_template: The template from which the body of the email is to be generated
    :type email: string
    :param to_email: list of Receivers' email. If not specified the email of the instance if passed is used
    :type to_email: list, tuple
    :param from_email: the Sender. The settings DEFAULT_FROM_EMAIL is used if this argument is not specified
    :type from_email: string
    :param instance_id: id of an instance from which the user and subscription object will be generated
    :type instance_id: int
    :param attachments: path of file to be attached to the email if any
    :type attachments: string
    :param context: extra context to be passed to the email template the dictionary to be parsed in the email
                    template
    :type context: dict
    """
    from project.models import User
    if not context:
        if username:
            context = {'user': User.objects.get(username=username)}
    body = render_to_string('emails/{0}'.format(email_template), context)
    message = EmailMessage(subject, body, from_email, to_email)
    message.content_subtype = "html"
    try:
        message.send()
    except Exception as exc:
        # Retry message sending if it fails. This automatically stops after 3 attempts and raises the error
        raise self.retry(exc=exc)


@app.task(bind=True)
def send_error_mail(self, subject, template, **kwargs):  # pylint: disable=unused-argument
    """ Sends Error message to sysadmin """

    send_email.delay(subject, template, to_email=[settings.SYSTEM_ADMIN_EMAIL, ], **kwargs)
