from dnaorder.forms import SubmissionForm, SubmissionStatusForm
from django.shortcuts import render, redirect
from dnaorder.models import SubmissionType, Submission, SubmissionStatus
from sendfile import sendfile
import tempfile
import os
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from dnaorder import emails
def submit(request):
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm()
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            emails.confirm_order(submission, request)
            return render(request,'submission.html',{'submission':submission,'editable':submission.editable(request.user),'submitted':True})
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

def update_submission(request,id):
    submission = Submission.objects.get(id=id)
    if not request.user.is_authenticated and not submission.editable():
        raise PermissionDenied
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm(instance=submission)
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES,instance=submission)
        if form.is_valid():
            submission = form.save(commit=True)
            return redirect('submission',id=id)
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

@login_required
def submissions(request):
    return render(request,'submissions.html',{})

def submission(request,id):
    submission = Submission.objects.get(id=id)
    status_form = SubmissionStatusForm(instance=submission) if request.user.is_authenticated else None
    return render(request,'submission.html',{'submission':submission,'status_form':status_form,'editable':submission.editable(request.user)})

def print_submission(request,id):
    submission = Submission.objects.get(id=id)
    return render(request,'print_submission.html',{'submission':submission})

def confirm_submission(request,id):
    submission = Submission.objects.get(id=id)
    if submission.status:
        return redirect('submission',id=id)
    submission.status = SubmissionStatus.objects.filter(default=True).order_by('order').first()
    submission.save()
    emails.order_confirmed(submission, request)
    return render(request,'submission.html',{'submission':submission,'editable':submission.editable(request.user),'confirmed':True})

def download(request,id):
    from django.http import HttpResponse
    from wsgiref.util import FileWrapper

    submission = Submission.objects.get(id=id)
    data = request.GET.get('data','samples')#samples, sra, or combined
    format = request.GET.get('format','original')
    filename = None
    if format == 'original':
        if data == 'sra':
            file_path = submission.sra_form.file.name
        else:
            file_path = submission.sample_form.file.name
    else:
        tmpfile = tempfile.NamedTemporaryFile()
        if data == 'sra':
            df = submission.sra_samplesheet.df
            filename = "%s.sra"%submission.id
        elif data == 'combined':
            df = submission.samplesheet.join(submission.sra_samplesheet)
            filename = "%s.combined"%submission.id
        else:
            df = submission.samplesheet.df
            filename = "%s.samples"%submission.id
#         print samplesheet
        #Make it all lower case.  Maybe this should be an option in the interface?
        df = df.apply(lambda x: x.str.lower(),axis='columns')
#         df = df[:][:].str.lower()
        if format == 'xlsx':
            #writer = ExcelWriter(tmpfile.name, engine='xlsxwriter')
            df.to_excel(tmpfile.name,engine='xlsxwriter',index=False)
            filename += '.xlsx'
        if format == 'csv':
            df.to_csv(tmpfile.name,index=False)
            filename += '.csv'
            
#         print 'read'
#         print os.path.exists(tmpfile.name)
#         print tmpfile.read()
        file_path = tmpfile.name
        
    print file_path
    # generate the file
    return sendfile(request, file_path, attachment_filename=filename,attachment=True)