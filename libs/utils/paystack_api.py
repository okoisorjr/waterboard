""" Important functions and utils used in code """
import random
import string

from django.conf import settings
from paystackapi.paystack import Paystack
from paystackapi.transaction import Transaction


class PaystackAccount:
    """ Paystack Transaction via Secret Key """

    # pylint: disable=no-self-use
    def __init__(self, email, public_key, amount):
        self.paystack_conn = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)
        self.__email = email
        self.__public_key = public_key
        self.__amount = amount * 100


    def get_response(self, reference):
        """
        Verifies transaction
        :param reference: unique transaction reference to be verified
        :returns: Status of Transation Success
        :rtype: bool
        """
        response = Transaction.verify(reference=reference)
        return response


    def verify_transaction(self, reference):
        """
        Verifies transaction
        :param reference: unique transaction reference to be verified
        :returns: Status of Transation Success
        :rtype: bool
        """
        response = self.get_response(reference)
        return response["status"]

    def charge(self, authorization_code, email, amount):
        """
        Used for recurring payments to charge a user based on his current subscription
        """
        response = Transaction.charge(
            reference=self.reference, authorization_code=authorization_code,
            email=email, amount=amount
            )
        return response["data"]["status"]

    def get_reference(self):
        """ returns a generated random reference token"""

        return ''.join(
            [random.choice(string.ascii_letters + string.digits) for n in range(16)]
        )

    @property
    def reference(self):
        """ returns a generated random reference token"""

        return self.get_reference()

    @property
    def email(self):
        return self.__email

    @property
    def public_key(self):
        return self.__public_key

    @property
    def amount(self):
        return self.__amount
