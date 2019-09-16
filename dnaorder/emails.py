from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def status_update(submission,request,emails=None):
    body = render_to_string('emails/status_update.txt',{'submission':submission},request=request)
    send_mail(
        'Submission {id} Status Updated'.format(id=submission.internal_id),
        body,
        submission.get_lab_from_email(),
        emails or [submission.email],
        fail_silently=False,
    )
def confirm_order(submission,request,emails=None):
    body = render_to_string('emails/confirm_order.txt',{'submission':submission},request=request)
    send_mail(
        'Please Confirm Your Submission',
        body,
        submission.get_lab_from_email(),
        emails or [submission.email],
        fail_silently=False,
    )
def order_confirmed(submission,request,emails=None):
    body = render_to_string('emails/order_confirmed.txt',{'submission':submission},request=request)
    send_mail(
        'Submission {id} received'.format(id=submission.internal_id),
        body,
        submission.get_lab_from_email(),
        emails or [submission.email,submission.pi_email] + submission.participant_emails,
        fail_silently=False,
    )

def note_email(note):
    body = render_to_string('emails/note.txt',{'note':note,'BASE_URI':settings.BASE_URI})
    send_mail(
        'A note has been added to submission {id}'.format(id=note.submission.internal_id),
        body,
        note.submission.get_lab_from_email(),
        note.emails,
        fail_silently=False,
    )