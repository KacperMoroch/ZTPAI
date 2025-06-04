from celery import shared_task
from django.core.mail import send_mail
import time

@shared_task
def send_registration_email(email):
    print(f"Wysyłam maila do: {email}")
    # time.sleep(10)
    subject = 'Witamy!'
    message = 'Dziękujemy za rejestrację w naszej aplikacji.'
    from_email = 'goaldle.noreply@gmail.com'
    send_mail(subject, message, from_email, [email])
