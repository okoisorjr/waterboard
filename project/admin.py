from django.contrib import admin
from project.models import Plans, Subscription, User
# Register your models here.
admin.site.register(User)
admin.site.register(Plans)
admin.site.register(Subscription)