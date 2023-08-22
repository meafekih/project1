from django.shortcuts import render, redirect
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ExtendUser as User, EmailConfiguration
from django.http import JsonResponse

@login_required
@csrf_exempt
def sendingEmail(request):
    if request.method == 'POST':
        try:
            user = request.user
            email_from = user.email
            app_password = user.app_password
            
            email_to = request.POST.get('email_to')
            subject = request.POST.get('subject')
            content = request.POST.get('content')

            smtp_server=user.email_conf.smtp_server
            smtp_port=user.email_conf.smtp_port
            attachment = request.FILES.get('attachment')

            sending(email_from, app_password, email_to,
                subject, content, smtp_server, smtp_port, attachment=attachment)
            
            return redirect('customers')
        except Exception as e:
            return JsonResponse({"message": str(e)}, status=500)
    else:
        return render(request, 'authentication/emailing.html')
    
def sending(email_from, app_password, email_to,
         subject, content, smtp_server, smtp_port, attachment=None):
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = email_from
        message["To"] = email_to

        part1 = MIMEText(content, "plain")
        message.attach(part1)


        if attachment:
            attached_file = MIMEApplication(attachment.read(), _subtype=attachment.content_type.split('/')[1])
            attached_file.add_header('content-disposition', 'attachment', filename=attachment.name)
            message.attach(attached_file)


        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
            server.login(email_from, app_password)
            server.sendmail(email_from, email_to, message.as_string())
    except Exception as e:
        print(e)