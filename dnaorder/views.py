from django.shortcuts import redirect
from dnaorder.models import SubmissionType, Submission, UserEmail
from rest_framework.decorators import api_view, permission_classes
from dnaorder.api.serializers import UserSerializer
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from dnaorder.validators import SamplesheetValidator
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from rest_framework.permissions import AllowAny
from dnaorder.spreadsheets import get_dataset, get_submission_dataset, get_cols
from django.http.response import HttpResponse
import tablib
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site

def login(request):
    print('process request', request.META)
    print('login', request.user)
    if request.user.is_authenticated:
        print('is authenticated')
        return redirect('/submissions/')
    else:
        print('authenticate?', request.META)
        # Should probably be relying on REMOTE USER using the following config in apache
        #OIDCRemoteUserClaim preferred_username
        remote_user = request.META.get('OIDC_CLAIM_preferred_username', request.META.get('OIDC_CLAIM_email'))
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
                UserEmail.objects.create(user=user, email=user.email)
#             if user is not None:
            auth_login(request, user)
            return redirect('/')
        # Is this all wrong? I'm authenticating but the logic is in middleware...
#         user = authenticate(request)
    return redirect('/')

def logout(request):
    print('logout', request.user)
    if request.user.is_authenticated:
        auth_logout(request)
    site = get_current_site(request)
    return redirect('/server/accounts/login/redirect?logout=https://{}/'.format(site.domain))

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
        return Response({'message':'Authentication failed.'},status=400)

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def get_user(request):
    if request.user.is_authenticated:
        user = request.user
        return Response({'status':'success','user':UserSerializer(instance=user).data})
    else:
        return Response({'message':'Not authenticated.'},status=403)

@api_view(['POST'])
def logout_view(request):
    auth_logout(request)
    return Response({'status':'success'})

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
        return Response({'errors':errors, 'warnings': warnings},status=400)

@permission_classes((AllowAny,))
def download(request, id):
    submission = Submission.objects.get(id=id)
    data = request.GET.get('data','combined')#samples or submission
    format = request.GET.get('format','xlsx')
    format = format if format in ['xls','xlsx','csv','tsv','json'] else 'xlsx'
    filename = None
    
    if data == 'submission':
        dataset = get_submission_dataset(submission)
        filename = "{0}.submission.{1}".format(submission.internal_id,format)
    elif data == 'all': #samples
        submission_data = get_submission_dataset(submission)
        submission_data.title = "Submission"
        table_cols = get_cols(submission.submission_schema, table=True)
        tables = [submission_data]
        for col in table_cols:
            table_data = get_dataset(submission.submission_schema.get('properties',{}).get(col,{}).get('schema',{}), submission.submission_data.get(col, []))
            table_data.title = col
            tables.append(table_data)
        dataset = tablib.Databook(tables)
        format = 'xlsx'
        filename = "{0}.{1}".format(submission.internal_id,format)
    else: #all
        dataset = get_dataset(submission.submission_schema.get('properties',{}).get(data,{}).get('schema',{}), submission.submission_data.get(data, []))
        dataset.title = data
        filename = "{0}.{1}.{2}".format(submission.internal_id,data,format)
    content_types = {'xls':'application/vnd.ms-excel','tsv':'text/tsv','csv':'text/csv','json':'text/json','xlsx':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    response_kwargs = {
            'content_type': content_types[format]
        }
    response = HttpResponse(getattr(dataset, format), **response_kwargs)
    response['Content-Disposition'] = 'attachment; filename={0}'.format(filename)
    return response
    # generate the file
#     return sendfile(request, file_path, attachment_filename=filename,attachment=True)

@api_view(['GET'])
@csrf_exempt
@permission_classes((AllowAny,))
def test(request):
    return Response({'message':'Test message'})