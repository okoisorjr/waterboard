from django import forms
from project.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    USER_TYPE = (
        ('Individual', 'Individual'),
        ('org', "Organization")
    )
    user_type = forms.ChoiceField(choices=USER_TYPE)
    first_name = forms.CharField(max_length=25, required=True)
    last_name = forms.CharField(max_length=25, required=True)
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'placeholder':'Phone numbers must start with country area code. E.g +2348811002'}
        )
        )
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = ['user_type', 'username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        # exclude = ['phone_number', 'is_ordinary', 'is_organization']