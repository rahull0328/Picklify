from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage
import os
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_account_activation_email(email, email_token):
    subject = "Activate Your Account - Welcome to Our Store!"
    email_from = settings.EMAIL_HOST_USER

    # Load the HTML template
    html_message = render_to_string("emails/account_activation.html", {"email_token": email_token})
    
    # Convert HTML to plain text
    plain_message = strip_tags(html_message)

    # Create email object
    email_message = EmailMultiAlternatives(subject, plain_message, email_from, [email])
    email_message.attach_alternative(html_message, "text/html")

    # Attach the image
    logo_path = os.path.join(settings.BASE_DIR, "public/static/img/logo.webp")
    try:
        with open(logo_path, "rb") as img_file:
            logo = MIMEImage(img_file.read(), _subtype="webp")
            logo.add_header("Content-ID", "<logo>")  # Content-ID for embedding
            logo.add_header("Content-Disposition", "inline", filename="logo.webp")
            email_message.attach(logo)
    except FileNotFoundError:
        print("Logo file not found. Ensure the path is correct.")

    # Send the email
    email_message.send()
    
def send_order_invoice_email(email, invoice_path, context):
    subject = "Your Order Invoice - Thank You for Shopping!"
    email_from = settings.EMAIL_HOST_USER

    # Load the HTML content
    html_message = render_to_string("emails/invoice.html", context)
    plain_message = strip_tags(html_message)

    # Use EmailMultiAlternatives to send both plain text and HTML
    email_message = EmailMultiAlternatives(subject, plain_message, email_from, [email])
    email_message.attach_alternative(html_message, "text/html")

    # Attach the PDF invoice
    try:
        with open(invoice_path, "rb") as invoice_file:
            email_message.attach("invoice.pdf", invoice_file.read(), "application/pdf")
    except FileNotFoundError:
        print("Invoice PDF not found. Email sent without attachment.")

    # Send the email
    email_message.send()
