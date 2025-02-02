from django.conf import settings
from django.core.mail import send_mail


def sendAccountActivationEmail(email, emailToken):
    subject = 'Account Activation Email !'
    emailFrom = settings.Email_MOST_USER
    message = f'Hi, Click on the below link to activate your account http://127.0.0.1:8000/accounts/activate/{emailToken}'
    send_mail(subject, message, emailFrom, [email])