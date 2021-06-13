""" 
Contains Models related to payments: Subscription, Plans
"""
import uuid
from django.db import models
from django.utils import timezone
from project.models import User

class Plans(models.Model):
    """
    Stores the plan details
    """

    name = models.CharField(max_length=127, primary_key=True)
    duration = models.PositiveIntegerField(default=30)
    price = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    long_name = models.CharField(max_length=127)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Plans'

    def __str__(self):
        return f'{self.long_name}'

    def __eq__(self, plan):
        if plan:
            return self.price == plan.price
        return super().__eq__(plan)

    def __gt__(self, plan):
        return self.price > plan.price

    def __lt__(self, plan):
        return self.price < plan.price



class Subscription(models.Model):
    """ the Subscription Details for the User

    User's subscriptions are dynamic. This means that a subscription is only active during
    the time a user has an active instance. If there is no active instance on the account,
    the subscription becomes paused.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='User Subscription'
    )

    plan_subscribed = models.ForeignKey(Plans, blank=True, null=True,
                                        on_delete=models.CASCADE, related_name="plan")
    activated = models.BooleanField(default=False)
    date_subscribed = models.DateTimeField(auto_now=False, auto_now_add=True)
    expiry_date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    active = models.BooleanField(default=False)
    is_organization = models.BooleanField(default=False)
    seconds_left = models.BigIntegerField(default=0)

    def __str__(self):
        return self.get_plan_subscribed_display()

    def deactivate(self):
        """ Deactivate Subscription"""
        self.active = False
        self.save()

    def activate(self):
        """ Activate Subscription"""
        self.active = True
        self.save()


    @property
    def plan(self):
        """ return the plan label

        :returns: Plan Model
        """
        return self.plan_subscribed


    def activate_subscription(self, plan):
        """ Activates an account for a certain subscription

           :param plan: A plan model object to be set as new subscription
        """
        # If account is expired, we want to add the new plan duration to the current time, not to the
        # user existing subscription
        if not (self.active and self.activated):
            self.expiry_date = timezone.now() + timezone.timedelta(plan.duration)
        else:
            self.expiry_date = self.expiry_date + timezone.timedelta(plan.duration)
        self.plan_subscribed = plan
        self.active = True
        self.activated = True
        self.save()

    def get_plan_subscribed_display(self):
        """ return plan long name """

        return self.plan.long_name


