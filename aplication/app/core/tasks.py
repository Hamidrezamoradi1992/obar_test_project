from celery import shared_task
from django.core.mail import send_mail



@shared_task
def send_email(subject, to_email, context, template_name=None):
    subject = subject
    message = context
    recipient_list = to_email
    print(f"SEND{context} {to_email}")
    send_mail(subject, message, None, recipient_list)
    print(f"COMPILED {context} {to_email}")

