from django.core.mail import send_mail
import random
from django.conf import settings

def send_otp(email):
    subject = 'Verification email'
    otp = random.randint(1000, 9999)
    message = f'Your OTP is: {otp}'
    email_from = settings.DEFAULT_FROM_EMAIL
    
    send_mail(subject, message, email_from, [email])