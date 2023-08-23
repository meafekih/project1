from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import smtplib, ssl
from apps.base.decorators import Rest_auth_required
from django.utils.html import escape

import imaplib
import email
from email.header import decode_header

@Rest_auth_required
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
            
            return JsonResponse({"success": True, "message": 'Email sent'}, status=200)
            #return redirect('customers')
        
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)
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
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@Rest_auth_required
def fetchingEmails(request):
    if request.method=='POST':
        pass
    else:        
        user = request.user
        email_from = user.email
        app_password = user.app_password
        
        imap_server=user.email_conf.incoming_server
        imap_port=user.email_conf.incoming_port
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)

        mail.login(email_from, app_password)
        mail.select("inbox")
        email_messages = fetch(mail)
        mail.logout()
    return render(request, 'authentication/email_messages.html', {'email_messages': email_messages})

def fetch(mail):
    email_messages = []
    status, email_ids = mail.search(None, "ALL")
    email_ids = email_ids[0].split()
    index = 0
    for email_id in email_ids:
        index +=1
        if index <=10:
            one_email = {}
            # Fetch the email
            status, msg_data = mail.fetch(email_id, "(RFC822)")
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)

            # Get email details
            from_address = email_message["From"]
            subject = email_message["Subject"]
            
            # Decode the subject if it's encoded
            decoded_subject, encoding = decode_header(subject)[0]
            if isinstance(decoded_subject, bytes):
                decoded_subject = decoded_subject.decode(encoding)
            
            print(f"From: {from_address}")
            print(f"Subject: {decoded_subject}")
            
            # If the email has multiple parts (e.g., attachments), you can further process them
            if email_message.is_multipart():
                for part in email_message.walk():
                    content_body=""
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    if "attachment" in content_disposition:
                        filename = part.get_filename()
                        if filename:
                            print(f"Attachment: {filename}")
                    else:
                        body = part.get_payload(decode=True)
                        if body:
                            content_body += escape(body.decode("utf-8")) +'\n'
                            print("Content:", escape(body.decode("utf-8"))) 


            one_email["from_address"]=from_address
            one_email["subject"]=subject
            one_email["body"]=body
            one_email["to"]=""
            one_email["date"]=""
            one_email["attachments"]=[]
            email_messages.append(one_email)

    return email_messages
# Close the mailbox and log out

