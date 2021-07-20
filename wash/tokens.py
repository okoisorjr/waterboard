from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
# from pip._vendor import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (str(user.pk) +
                str(timestamp) +
                str(user.email))


account_activation_token = AccountActivationTokenGenerator()