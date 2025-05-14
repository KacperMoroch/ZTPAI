from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_registration_email(email):
    print(f"Wysyłam maila do: {email}")
    subject = 'Witamy!'
    message = 'Dziękujemy za rejestrację w naszej aplikacji.'
    from_email = 'goaldle.noreply@gmail.com'
    send_mail(subject, message, from_email, [email])
