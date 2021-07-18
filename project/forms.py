from django import forms
from project.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['address'].required = True
        self.fields['city'].required = True


    USER_TYPE = (
        ('Individual', 'Individual'),
        ('org', "Organization")
    )
    user_type = forms.ChoiceField(choices=USER_TYPE)
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(
        attrs={'placeholder':'Phone numbers must start with country area code. E.g +2348811002'}
        )
        )
    class Meta(UserCreationForm.Meta):
        
        model = User
        fields = [
            'user_type', 'username', 'email', 'first_name', 'last_name', 'phone_number',
            'address', 'city', 'password1', 'password2'
            ]
        
    def save(self, commit: bool):
        if commit:
            user = super().save(commit=commit)
            user.is_active=False
            if self.cleaned_data.get('user_type') == "org":
                user.is_organization = True
                user.save()
            else:
                user.is_ordinary = True
                user.save()
        return user