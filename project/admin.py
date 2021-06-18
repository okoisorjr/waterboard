from django.contrib import admin
from project.models import Plans, Subscription, User
# Register your models here.

class SubscriptionInline(admin.StackedInline):
    """ Subscription model inline display for User Model """

    model = Subscription
    verbose_name_plural = 'subscriptions'


class UserAdmin(admin.ModelAdmin):
    """ Customized User Model display to include user profile, referral, instances and subscripiton """

    list_display = ('username', 'first_name', 'email')
    inlines = (
        SubscriptionInline,
    )


admin.site.register(User, UserAdmin)
admin.site.register(Plans)
