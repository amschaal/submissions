from dnaorder.forms import SubmissionForm
from django.shortcuts import render
from dnaorder.models import SubmissionType

def submission(request):
    submission_types = SubmissionType.objects.all()
    if request.method == 'GET':
        form = SubmissionForm()
    elif request.method == 'POST':
        form = SubmissionForm(request.POST,request.FILES)
        if form.is_valid():
            submission = form.save(commit=True)
            return render(request,'submitted.html',{'submission':submission})
    return render(request,'submission_form.html',{'form':form,'submission_types':submission_types})