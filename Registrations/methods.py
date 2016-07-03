import random
import string
from django.core.mail import send_mail, BadHeaderError, EmailMessage

__author__ = 'Saad'


class xml:
    def __init__(self, name, value):
        self.name = name
        self.value = value


def random_string(length):
    pool = string.letters + string.digits
    return ''.join(random.choice(pool) for i in xrange(length))


def send_email(subject, message, to_email, from_email='findmyrideapp@gmail.com'):
    if subject and message and from_email:
            msg = EmailMessage(subject, message, from_email, to_email)
            msg.content_subtype = "html"
            try:
                msg.send()
            except:
                j = None
