from django.core.mail import send_mail
from django.template.loader import render_to_string
def status_update(submission,request,emails=None):
    body = render_to_string('emails/status_update.txt',{'submission':submission},request=request)
    send_mail(
        'Order Status Updated',
        body,
        'dnatech@ucdavis.edu',
        emails or [submission.email],
        fail_silently=False,
    )