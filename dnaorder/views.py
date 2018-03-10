from dnaorder.forms import SubmissionForm, UpdateSubmissionForm,\
    SubmissionStatusForm
from django.shortcuts import render, redirect
from dnaorder.models import SubmissionType, Submission
from sendfile import sendfile
import tempfile
import os
import json
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def submission(request):
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm()
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            return render(request,'order.html',{'order':submission,'submitted':True})
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

def update_submission(request,id):
    submission = Submission.objects.get(id=id)
    if not request.user.is_authenticated and not submission.editable():
        raise PermissionDenied
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = UpdateSubmissionForm(instance=submission)
    elif request.method == 'POST':
        form = UpdateSubmissionForm(request.POST,request.FILES,instance=submission)
        if form.is_valid():
            submission = form.save(commit=True)
            return redirect('order',id=id)
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

@login_required
def orders(request):
    return render(request,'orders.html',{})

def order(request,id):
    order = Submission.objects.get(id=id)
    status_form = SubmissionStatusForm(instance=order) if request.user.is_authenticated else None
    return render(request,'order.html',{'order':order,'status_form':status_form})

def download(request,id):
    from django.http import HttpResponse
    from wsgiref.util import FileWrapper

    order = Submission.objects.get(id=id)
    data = request.GET.get('data','samples')#samples, sra, or combined
    format = request.GET.get('format','original')
    filename = None
    if format == 'original':
        if data == 'sra':
            file_path = order.sra_form.file.name
        else:
            file_path = order.sample_form.file.name
    else:
        tmpfile = tempfile.NamedTemporaryFile()
        if data == 'sra':
            df = order.sra_samplesheet.df
            filename = "%s.sra"%order.id
        elif data == 'combined':
            df = order.samplesheet.join(order.sra_samplesheet)
            filename = "%s.combined"%order.id
        else:
            df = order.samplesheet.df
            filename = "%s.samples"%order.id
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