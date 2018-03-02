from dnaorder.forms import SubmissionForm
from django.shortcuts import render
from dnaorder.models import SubmissionType, Submission
from sendfile import sendfile
import tempfile
import os
import json

def submission(request):
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm()
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            return render(request,'submitted.html',{'submission':submission,'samples':form._sample_ids})
#         else:
#             samplesheet = getattr(form, 'samplesheet',None)
#             sample_data = json.dumps(samplesheet.data) if samplesheet else None
#             sample_headers = json.dumps(samplesheet.headers) if samplesheet else None
#             sample_errors = json.dumps(samplesheet.error_lookup()) if samplesheet else None
#             sra_samplesheet = getattr(form, 'sra_samplesheet',None)
#             sra_sample_data = json.dumps(sra_samplesheet.data) if sra_samplesheet else None
#             sra_sample_headers = json.dumps(sra_samplesheet.headers) if sra_samplesheet else None
#             sra_sample_errors = json.dumps(sra_samplesheet.error_lookup()) if sra_samplesheet else None
#             return render(request,'submission_form.html',{'form':form,'submission_types':submission_types,'sample_data':sample_data,'sample_headers':sample_headers,'sample_errors':sample_errors,'sra_sample_data':sra_sample_data,'sra_sample_headers':sra_sample_headers,'sra_sample_errors':sra_sample_errors})
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})

def orders(request):
    return render(request,'orders.html',{})

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