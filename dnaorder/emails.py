from django.core.mail import send_mail
from django.template.loader import render_to_string
def status_update(submission,request,emails=None):
    body = render_to_string('emails/status_update.txt',{'submission':submission},request=request)
    send_mail(
        'Submission Status Updated',
        body,
        'dnatech@ucdavis.edu',
        emails or [submission.email],
        fail_silently=False,
    )
def confirm_order(submission,request,emails=None):
    body = render_to_string('emails/confirm_order.txt',{'submission':submission},request=request)
    send_mail(
        'Please Confirm Your Submission',
        body,
        'dnatech@ucdavis.edu',
        emails or [submission.email],
        fail_silently=False,
    )
def order_confirmed(submission,request,emails=None):
    body = render_to_string('emails/order_confirmed.txt',{'submission':submission},request=request)
    send_mail(
        'Submission {id} confirmed'.format(id=submission.id),
        body,
        'dnatech@ucdavis.edu',
        emails or [submission.email,submission.pi_email,'dnatech@ucdavis.edu'],
        fail_silently=False,
    )