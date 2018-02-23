from dnaorder.forms import SubmissionForm
from django.shortcuts import render
from dnaorder.models import SubmissionType, Submission
from sendfile import sendfile
import tempfile
import os

def submission(request):
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm()
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            return render(request,'submitted.html',{'submission':submission,'samples':form._sample_ids})
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

def orders(request):
    orders = Submission.objects.all().order_by('-submitted')
    return render(request,'orders.html',{'orders':orders})

def order(request,id):
    order = Submission.objects.get(id=id)
    return render(request,'order.html',{'order':order})

def download(request,id):
    from django.http import HttpResponse
    from wsgiref.util import FileWrapper

    order = Submission.objects.get(id=id)
    data = request.GET.get('data','samples')#samples, sra, or combined
    format = request.GET.get('format','original')
    filename = None
    if format == 'csv':
        tmpfile = tempfile.NamedTemporaryFile()
        print tmpfile.name
        if data == 'sra':
            samplesheet = order.sra_samplesheet
            filename = "SRA.%s.csv"%order.id
        else:
            samplesheet = order.samplesheet
            filename = "samples.%s.csv"%order.id
#         print samplesheet
#         print samplesheet.df.to_csv()
        samplesheet.df.to_csv(tmpfile.name)
        print 'read'
        print os.path.exists(tmpfile.name)
        print tmpfile.read()
        file_path = tmpfile.name
    else:
        if data == 'sra':
            file_path = order.sra_form.file.name
        else:
            file_path = order.sample_form.file.name
        
        
    print file_path
    # generate the file
    return sendfile(request, file_path, attachment_filename=filename,attachment=True)