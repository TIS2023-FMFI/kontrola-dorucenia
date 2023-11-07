from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from django.core.mail import EmailMessage, get_connection
from django.conf import settings

workbook = pd.read_excel('../example.xls')

def index(request):
    try:
        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            subject = request.POST.get("subject")
            email_from = settings.EMAIL_HOST_USER
            recipient_list = ["t402829@gmail.com"]
            message = request.POST.get("message")
            email = EmailMessage(subject, message, email_from, recipient_list, connection=connection)
            sent = email.send()

            # Check if the email was sent successfully and handle accordingly
            if sent:
                return HttpResponse("Email sent successfully.")
            else:
                return HttpResponse("Email not sent.")

    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}")
