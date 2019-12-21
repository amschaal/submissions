from dnaorder.forms import CustomPrintForm 
from django.shortcuts import render, redirect
from dnaorder.models import SubmissionType, Submission
from sendfile import sendfile
import tempfile
from django.contrib.auth.decorators import login_required
from dnaorder import emails
from collections import OrderedDict
from rest_framework.decorators import api_view, permission_classes
from dnaorder.api.serializers import SubmissionSerializer, UserSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from dnaorder.validators import SamplesheetValidator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny
from dnaorder.spreadsheets import get_dataset, get_submission_dataset
from django.http.response import HttpResponse
import tablib
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

def login(request):
    print('login', request.user)
    if request.user.is_authenticated:
        print('is authenticated')
        return redirect('/submissions/')
    else:
        print('authenticate?')
        remote_user = request.META.get('OIDC_CLAIM_username')
        print('remote_user', remote_user)
        if remote_user:
#             user = User.objects.filter(username=remote_user).first()
            user, created = User.objects.get_or_create(username=remote_user)
            if created:
                print('user created')
                user.email = request.META.get('OIDC_CLAIM_email')
                user.last_name = request.META.get('OIDC_CLAIM_family_name')
                user.first_name = request.META.get('OIDC_CLAIM_given_name')
                user.save()
#             if user is not None:
            auth_login(request, user)
            return redirect('/submissions/')
        # Is this all wrong? I'm authenticating but the logic is in middleware...
#         user = authenticate(request)
    return redirect('/')
    
#     else:

@api_view(['POST'])
@csrf_exempt
@permission_classes((AllowAny,))
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if request.user.is_authenticated and not username:
        user = request.user
    else:
        user = authenticate(request._request, username=username, password=password)
    if user is not None:
        auth_login(request._request, user)
        return Response({'status':'success','user':UserSerializer(instance=user).data})
    else:
        return Response({'message':'Authentication failed.'},status=500)

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({'status':'success','user':UserSerializer(instance=user).data})
    else:
        return Response({'message':'Not authenticated.'},status=500)

@api_view(['POST'])
def logout_view(request):
    auth_logout(request)
    return Response({'status':'success'})

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def submit(request):
#     submission_types = SubmissionType.objects.all()
#     form = SubmissionForm(request.data)
#     if form.is_valid():
#         submission = form.save(commit=True)
#         submission_serializer = SubmissionSerializer(instance=submission)
#         return Response(submission_serializer.data)
#     return Response({'errors':form.errors},status=500)
# 
# def static_submit(request):
#     submission_types = SubmissionType.objects.all()
#     if request.method == 'GET':
#         form = SubmissionForm()
#     elif request.method == 'POST':
#         form = SubmissionForm(request.POST,request.FILES)
#         if form.is_valid():
#             submission = form.save(commit=True)
#             emails.confirm_order(submission, request)
#             return render(request,'submission.html',{'submission':submission,'editable':submission.editable(request.user),'submitted':True})
#     return render(request,'submission_form_hot.html',{'form':form,'submission_types':submission_types})
# 
# # @csrf_exempt
# @api_view(['PUT'])
# @permission_classes([AllowAny])
# def update_submission(request,id):
#     form_class = AdminSubmissionForm if request.user.is_staff else SubmissionForm
#     submission = Submission.objects.get(id=id)
# #     if not request.user.is_authenticated and not submission.editable():
# #         raise PermissionDenied
#     form = form_class(request.data,instance=submission)
#     if form.is_valid():
#         submission = form.save(commit=True)
#         submission_serializer = SubmissionSerializer(instance=submission,context={'request':request})
#         return Response(submission_serializer.data)
#     return Response({'errors':form.errors},status=500)
# 
# def submission_types(request):
#     submission_types = SubmissionType.objects.filter(show=True)
#     return render(request,'submission_types.html',{'submission_types':submission_types})
# 
# def submission_type_versions(request,id):
#     submission_type = SubmissionType.objects.get(id=id)
#     return render(request,'submission_type_versions.html',{'submission_type':submission_type})
# 
# def create_update_submission_type(request,id=None):
#     submission_type = SubmissionType.objects.get(id=id) if id else None
#     if request.method == 'GET':
#         form = SubmissionTypeForm(instance=submission_type)
#     elif request.method == 'POST':
#         form = SubmissionTypeForm(request.POST,request.FILES,instance=submission_type)
#         if form.is_valid():
#             submission_type = form.save(request.user,commit=True)
#             if id and int(id) != submission_type.id:
#                 return redirect('update_submission_type',id=submission_type.id)
#             return render(request,'submission_type_form.html',{'form':form,'submission_type':submission_type,'valid':True})
#     return render(request,'submission_type_form.html',{'form':form,'submission_type':submission_type})

# def validators(request):
#     validators = Validator.objects.all().order_by('field_id')
#     return render(request,'validators.html',{'validators':validators})
# 
# def create_update_validator(request,id=None):
#     validator = Validator.objects.get(id=id) if id else None
#     if request.method == 'GET':
#         form = ValidatorForm(instance=validator)
#     elif request.method == 'POST':
#         form = ValidatorForm(request.POST,request.FILES,instance=validator)
#         if form.is_valid():
#             validator = form.save(commit=True)
#             return render(request,'validator_form.html',{'form':form,'validator':validator,'valid':True})
#     return render(request,'validator_form.html',{'form':form,'validator':validator})
# 
# @login_required
# def submissions(request):
#     return render(request,'submissions.html',{})
# 
# def submission(request,id):
#     submission = Submission.objects.get(id=id)
#     status_form = SubmissionStatusForm(instance=submission) if request.user.is_authenticated else None
#     return render(request,'submission.html',{'submission':submission,'status_form':status_form,'editable':submission.editable(request.user)})

def print_submission(request,id):
    submission = Submission.objects.get(id=id)
    exclude = submission.type.excluded_fields if not 'exclude' in request.GET else request.GET.getlist('exclude')
    max_samples = request.GET.get('max_samples')
    if not max_samples:
        max_samples = 1000
    variables = [v.replace('_',' ') for v in submission.samplesheet.headers if v not in exclude]#list(set(submission.samplesheet.headers)-set(exclude))
    vertical = 'vertical' in request.GET
    pages = submission.samplesheet.get_data(transpose=vertical,exclude_columns=exclude,page_size=int(max_samples))
    
    if vertical:
        pages = [OrderedDict(zip(variables,page)) for page in pages]
    return render(request,'print_submission.html',{'submission':submission,'variables':variables,'pages':pages,'vertical':vertical})

def customize_print(request,id):
    submission = Submission.objects.get(id=id)
    form = CustomPrintForm(submission,initial={'exclude':submission.type.excluded_fields})
    return render(request,'customize_print.html',{'submission':submission,'form':form})

# def confirm_submission(request,id):
#     submission = Submission.objects.get(id=id)
#     url = '{0}{1}'.format(settings.BASE_URI,submission.get_absolute_url())
#     if not submission.confirmed:
#         submission.confirmed = timezone.now()
#         submission.save()
#         emails.order_confirmed(submission, request)
#     return redirect(url)

def download_old(request,id):
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
            
        file_path = tmpfile.name
        
    # generate the file
    return sendfile(request, file_path, attachment_filename=filename,attachment=True)

@api_view(['POST'])
@permission_classes((AllowAny,))
def validate_data(request,type_id=None):
    if type_id:
        schema = SubmissionType.objects.get(id=type).sample_schema
    else:
        schema = request.data.get('sample_schema')
    validator = SamplesheetValidator(schema,request.data.get('data'))
    errors, warnings = validator.validate() #validate_samplesheet(submission_type.schema,request.data.get('data'))
    if len(errors) == 0 and len(warnings) == 0:
        return Response({'status':'success','message':'The data was successfully validated'})
    else:
        return Response({'errors':errors, 'warnings': warnings},status=500)

@permission_classes((AllowAny,))
def download(request, id):
    submission = Submission.objects.get(id=id)
    data = request.GET.get('data','combined')#samples or submission
    format = request.GET.get('format','xlsx')
    format = format if format in ['xls','xlsx','csv','tsv','json'] else 'xls'
    filename = None
    
    if data == 'submission':
        dataset = get_submission_dataset(submission)
        filename = "{0}.submission.{1}".format(submission.id,format)
    elif data == 'samples': #samples
        dataset = get_dataset(submission.sample_schema, submission.sample_data)
        filename = "{0}.samples.{1}".format(submission.id,format)
    else: #all
        submission_data = get_submission_dataset(submission)
        sample_data = get_dataset(submission.sample_schema, submission.sample_data)
        submission_data.title = "Submission"
        sample_data.title = "Samples"
        dataset = tablib.Databook((submission_data,sample_data))
        format = 'xlsx'
        filename = "{0}.{1}".format(submission.id,format)
    content_types = {'xls':'application/vnd.ms-excel','tsv':'text/tsv','csv':'text/csv','json':'text/json','xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    response_kwargs = {
            'content_type': content_types[format]
        }
    response = HttpResponse(getattr(dataset, format), **response_kwargs)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
    # generate the file
#     return sendfile(request, file_path, attachment_filename=filename,attachment=True)