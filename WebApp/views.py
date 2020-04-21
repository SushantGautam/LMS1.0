import glob
import json
import os
import re
import uuid
import zipfile  # For import/export of compressed zip folder
from datetime import datetime, timedelta
from json import JSONDecodeError

import cloudinary
import cloudinary.api
import cloudinary.uploader
import pandas as pd
import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import CommonPasswordValidator
from django.contrib.auth.views import LogoutView, LoginView, PasswordContextMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django_datatables_view.base_datatable_view import BaseDatatableView

from LMS.auth_views import CourseAuthMxnCls, AdminAuthMxnCls, AuthCheck, CourseAuth, MemberAuthMxnCls, \
    GroupMappingAuthMxnCls, InningInfoAuthMxnCls, InningGroupAuthMxnCls, ChapterAuthMxnCls, AssignmentInfoAuthMxnCls
from LMS.settings import BASE_DIR
from forum.models import Thread, Topic
from forum.views import get_top_thread_keywords, NodeGroup
from quiz.models import Quiz
from survey.models import SurveyInfo
from .forms import CenterInfoForm, CourseInfoForm, ChapterInfoForm, SessionInfoForm, InningInfoForm, UserRegisterForm, \
    AssignmentInfoForm, QuestionInfoForm, AssignAssignmentInfoForm, MessageInfoForm, \
    AssignAnswerInfoForm, InningGroupForm, GroupMappingForm, MemberInfoForm, ChangeOthersPasswordForm, MemberUpdateForm, \
    InningManagerForm
from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, AssignmentQuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, Events, \
    InningManager, Notice, NoticeView


class Changestate(View):
    def post(self, request):
        quizid = self.request.POST["quiz_id"]
        my_quiz = Quiz.objects.get(id=quizid)
        pre_test = self.request.POST.get("pre-test-radio", None)
        post_test = self.request.POST.get("post-test-radio", None)
        if (pre_test == '0' or post_test == '0'):
            my_quiz.draft = True
        elif (pre_test == '1' or post_test == '1'):
            my_quiz.draft = False

        my_quiz.save()
        return JsonResponse({'message': 'success'}, status=200)


class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


def ProfileView(request):
    if AuthCheck(request, admn=1) == 2:
        return redirect('login')
    return render(request, 'WebApp/profile.html')


def login(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          extra_context=None, redirect_authenticated_user=True):
    return LoginView.as_view(
        template_name=template_name,
        redirect_field_name=redirect_field_name,
        form_class=authentication_form,
        extra_context=extra_context,
        redirect_authenticated_user=redirect_authenticated_user,
    )(request)


def logout(request, next_page=None,
           template_name='logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           extra_context=None):
    return LogoutView.as_view(
        next_page=next_page,
        template_name=template_name,
        redirect_field_name=redirect_field_name,
        extra_context=extra_context,
    )(request)


_sentinel = object()


def error_400(request, exception):
    data = {}
    return render(request, 'error_page/page_400.html', data)


def error_403(request, exception):
    data = {}
    return render(request, 'error_page/page_403.html', data)


def error_404(request, exception):
    data = {}
    return render(request, 'error_page/page_404.html', data)


def error_500(request):
    data = {}
    return render(request, 'error_page/page_500.html', data)


def calendar(request):
    all_events = Events.objects.all()

    get_event_types = Events.objects.only('event_type')
    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:
        event_arr = []
        if request.GET.get('event_type') == "all":
            all_events = Events.objects.all()
        else:
            all_events = Events.objects.filter(event_type__icontains=request.GET.get('event_type'))

        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.event_name
            start_date = datetime.strptime(str(i.start_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(str(i.end_date.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr))

    # print(context['events'])
    return render(request, 'WebApp/calendar.html', {'events': all_events, "get_event_types": get_event_types})


def start(request):
    """Start page with a documentation.
    """
    # return render(request,"start.html")

    if request.user.is_authenticated:
        if not request.user.Use_Flag:
            logout(request)
            messages.add_message(request, messages.ERROR, 'Your account is deactivated. Please contact admin.')
            return redirect('login')

        if not request.user.Center_Code:
            logout(request)
            messages.add_message(request, messages.ERROR, 'No center assigned. Please contact admin.')
            return redirect('login')

        if request.user.Is_CenterAdmin:
            thread = Thread.objects.visible().filter(user__Center_Code=request.user.Center_Code).order_by('-pub_date')[
                     :5]
            wordCloud = Thread.objects.filter(user__Center_Code=request.user.Center_Code)
            thread_keywords = get_top_thread_keywords(request, 10)
            course = CourseInfo.objects.filter(Use_Flag=True, Center_Code=request.user.Center_Code).order_by(
                '-Register_DateTime')[:5]
            coursecount = CourseInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True).count
            studentcount = MemberInfo.objects.filter(Is_Student=True, Center_Code=request.user.Center_Code).count
            teachercount = MemberInfo.objects.filter(Is_Teacher=True, Center_Code=request.user.Center_Code).count
            threadcount = Thread.objects.visible().filter(user__Center_Code=request.user.Center_Code).count
            totalcount = MemberInfo.objects.filter(Center_Code=request.user.Center_Code).count
            surveys = SurveyInfo.objects.filter(Q(Use_Flag=True),
                                                Q(Center_Code=request.user.Center_Code) | Q(Center_Code=None),
                                                Q(End_Date__gte=datetime.now()))[:5]
            surveycount = SurveyInfo.objects.filter(Q(Use_Flag=True),
                                                    Q(Center_Code=request.user.Center_Code) | Q(Center_Code=None),
                                                    Q(End_Date__gte=datetime.now())).count
            sessions = InningInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True,
                                                 End_Date__gte=datetime.now())[:5]
            sessioncount = InningInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True,
                                                     End_Date__gte=datetime.now()).count

            if Notice.objects.filter(Start_Date__lte=datetime.now(), End_Date__gte=datetime.now(),
                                     status=True).exists():
                notice = \
                    Notice.objects.filter(Start_Date__lte=datetime.now(), End_Date__gte=datetime.now(), status=True)[0]
                if NoticeView.objects.filter(notice_code=notice, user_code=request.user).exists():
                    notice_view_flag = NoticeView.objects.filter(notice_code=notice, user_code=request.user)[
                        0].dont_show
                    if notice_view_flag:
                        notice = None
            else:
                notice = None
            # return HttpResponse("default home")
            return render(request, "WebApp/homepage.html",
                          {'course': course, 'coursecount': coursecount, 'studentcount': studentcount,
                           'teachercount': teachercount,
                           'threadcount': threadcount, 'totalcount': totalcount, 'thread': thread,
                           'wordCloud': wordCloud, 'get_top_thread_keywords': thread_keywords,
                           'surveys': surveys,
                           'surveycount': surveycount,
                           'sessions': sessions,
                           'sessioncount': sessioncount,
                           'notice': notice})
        elif request.user.Is_Teacher:
            return redirect('teacher_home')
        elif request.user.Is_Student:
            return redirect('student_home')
        # elif request.user.Is_Parent:
        #     return redirect('parent_home')
        else:
            logout(request)
            messages.add_message(request, messages.ERROR,
                                 'You are not assigned to any member type. Please contact admin.')
            return redirect('login')

    else:
        return render(request, "WebApp/splash_page.html")


# Profile page functions
def edit_basic_info_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = MemberInfo.objects.get(pk=request.user.id)
            if request.POST['username']:
                obj.username = request.POST['username']
            obj.first_name = request.POST['first_name']
            obj.last_name = request.POST['last_name']
            obj.Member_BirthDate = request.POST['Member_BirthDate']
            obj.Member_Gender = request.POST['Member_Gender']
            obj.save()
            messages.success(request, 'Profile basic info updated.')
            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
        except MemberInfo.DoesNotExist:
            messages.error(request, "Object doesn't exist")
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        messages.error(request, 'Not a valid request')
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def edit_contact_info_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = MemberInfo.objects.get(pk=request.user.id)
            obj.email = request.POST['email']
            obj.Member_Phone = request.POST['Member_Phone']
            obj.Member_Temporary_Address = request.POST['Member_Temporary_Address']
            obj.Member_Permanent_Address = request.POST['Member_Permanent_Address']
            obj.save()
            messages.success(request, 'Profile Contact details updated.')
            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
        except MemberInfo.DoesNotExist:
            messages.error(request, "Object doesn't exist")
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        messages.error(request, 'Not a valid request')
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def edit_description_info_ajax(request):
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = MemberInfo.objects.get(pk=request.user.id)
            obj.Member_Memo = request.POST['Member_Memo']
            obj.save()
            messages.success(request, 'Profile Description updated.')
            return JsonResponse({'status': 'Success', 'msg': 'save successfully'})
        except MemberInfo.DoesNotExist:
            messages.error(request, "Object doesn't exist")
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
    else:
        messages.error(request, 'Not a valid request')
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def edit_profile_image_ajax(request):
    if request.method == 'POST' and request.FILES['Member_Avatar']:
        try:
            obj = MemberInfo.objects.get(pk=request.user.id)
            media = request.FILES['Member_Avatar']
            if media.size / 1024 > 2048:
                messages.error(request, "Can't upload File size exceeds 2MB")
                return JsonResponse(data={'status': 'Fail', "msg": "File size exceeds 2MB"}, status=500)
            path = settings.MEDIA_ROOT
            name = (str(uuid.uuid4())).replace('-', '') + '.' + media.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/Member_images/')
            filename = fs.save(name, media)
            obj.Member_Avatar = 'Member_images/' + name
            obj.save()
            messages.success(request, 'Profile picture updated.')
            return JsonResponse({'status': 'Success', 'msg': 'Profile Picture Uploaded successfully'})
        except MemberInfo.DoesNotExist:
            messages.error(request, "Object doesn't exist")
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})
        except:
            messages.error(request, "Error Occured try agian")
            return JsonResponse({'status': "Fail", 'msg': "Some error occured try again"})
    else:
        messages.error(request, 'Not a valid request')
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


class register(CreateView):
    model = MemberInfo
    form_class = UserRegisterForm
    success_url = reverse_lazy('loginsuccess')
    template_name = 'registration/register.html'

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save(commit=False)

            username = self.request.POST.get('username')
            password = self.request.POST.get('password1')

            member_type = self.request.POST.get('member_type')
            print(self.request.POST.get('member_type'))
            if member_type == "Is_Teacher":
                self.object.Is_Teacher = True
            elif member_type == "Is_Student":
                self.object.Is_Student = True
            self.object.save()
            return redirect('loginsuccess')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['centers'] = CenterInfo.objects.all()
        return context


def change_password_others(request, pk):
    if request.method == 'POST':
        form = ChangeOthersPasswordForm(request.POST)
        if form.is_valid():
            # user = form.save()
            user = MemberInfo.objects.get(pk=pk)
            print(form.cleaned_data.get("password"), "  of user", user.username)
            user.set_password(form.cleaned_data.get("password"))
            user.save()

            # update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Password is changed successfully!')

            return redirect('memberinfo_detail', pk=pk)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ChangeOthersPasswordForm()
    return render(request, 'registration/change_password.html', {
        'form': form, 'usr': MemberInfo.objects.get(pk=pk)
    })


def loginsuccess(request):
    return render(request, "registration/registrationsuccessful.html")


class CenterInfoListView(ListView):
    model = CenterInfo


class CenterInfoCreateView(CreateView):
    model = CenterInfo
    form_class = CenterInfoForm


class CenterInfoDetailView(DetailView):
    model = CenterInfo


class CenterInfoUpdateView(UpdateView):
    model = CenterInfo
    form_class = CenterInfoForm


def CenterInfoDeleteView(request, pk):
    CenterInfo.objects.filter(pk=pk).delete()
    return redirect("centerinfo_list")


class MemberInfoListView(TemplateView):
    template_name = "WebApp/memberinfo_list.html"
    # model = MemberInfo
    #
    # def get_queryset(self):
    #     return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code, Use_Flag=True)


class MemberInfoListViewAjax(BaseDatatableView):
    model = MemberInfo
    counter = 0
    template_name = "WebApp/memberinfo_list.html"
    columns = ['counter', 'username', 'Member_ID', 'full_name', 'first_name', 'last_name', 'email', 'Member_Phone',
               'Member_Gender', 'Is_Student', 'Is_Teacher', 'Member_Permanent_Address', 'Member_Temporary_Address',
               'Member_BirthDate', 'type', 'action']
    order_columns = ['', 'username', 'Member_ID', '', 'first_name', 'last_name', 'email', 'Member_Phone',
                     'Member_Gender', 'Is_Student', 'Is_Teacher', '', '', '', '', '']

    def get_initial_queryset(self):
        return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code, Use_Flag=True)

    def render_column(self, row, column):
        # We want to render user as a custom column
        if column == "counter":
            self.counter += 1
            return self.counter
        elif column == 'full_name':
            # escape HTML for security reasons
            return escape('{0} {1}'.format(row.first_name, row.last_name))
        elif column == 'type':
            return row.get_user_type
        elif column == 'action':
            return '<a class="btn btn-sm btn-info" href="%s">Edit</a>  \
                    <a class="btn btn-sm btn-danger confirm-delete" id="%s">Delete</a>' % (row.get_update_url(), row.id)
        else:
            return super(MemberInfoListViewAjax, self).render_column(row, column)

    def filter_queryset(self, qs):
        # use parameters passed in GET request to filter queryset

        # simple example:
        search = self.request.GET.get('search[value]', None)
        onlystudents = self.request.GET.get('onlystudents', None)
        onlyteachers = self.request.GET.get('onlyteachers', None)
        if search:
            qs = qs.filter(username__istartswith=search) | qs.filter(first_name__istartswith=search) | qs.filter(
                last_name__istartswith=search) | qs.filter(email__istartswith=search) | qs.filter(
                Member_Phone__istartswith=search)
        if onlystudents:
            qs = qs.filter(Is_Student=True)
        if onlyteachers:
            qs = qs.filter(Is_Teacher=True)
        return qs.filter(Center_Code=self.request.user.Center_Code, Use_Flag=True)


class MemberInfoListViewInactive(ListView):
    model = MemberInfo
    template_name = 'WebApp/memberinfo_list_inactive.html'

    def get_queryset(self):
        return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code, Use_Flag=False)


class MemberInfoCreateView(CreateView):
    model = MemberInfo
    form_class = MemberInfoForm
    success_url = reverse_lazy('memberinfo_list')

    def form_valid(self, form):
        if form.is_valid():
            obj = form.save(commit=False)
            obj.Center_Code = self.request.user.Center_Code
            obj.password = make_password(obj.password)
            obj.Use_Flag = True
            obj.save()
            messages.success(self.request, 'New Member created successfully')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Error in creating member')
            print(form.errors)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': MemberInfo.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'A user with this username already exists.'
    return JsonResponse(data)


def validate_password(request):
    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    u = CommonPasswordValidator()
    try:
        u.validate(password, username)
        return JsonResponse("", safe=False)
    except ValidationError as e:
        return JsonResponse(e.messages, safe=False)


def MemberInfoActivate(request, pk):
    try:
        obj = MemberInfo.objects.get(pk=pk)
        obj.Use_Flag = True
        obj.save()
        messages.success(request, 'Member is activated sucessfully')
    except:
        messages.error(request, 'Cannot perform the action. Please try again later')

    if (request.POST['url']):
        return redirect(request.POST['url'])
    else:
        return redirect('memberinfo_detail', pk=pk)


def MemberInfoDeactivate(request, pk):
    try:
        obj = MemberInfo.objects.get(pk=pk)
        obj.Use_Flag = False
        obj.save()
        messages.success(request, 'Member is deactivated sucessfully')
    except:
        messages.error(request, 'Cannot perform the action. Please try again later')

    return redirect('memberinfo_detail', pk=pk)


# The following function is for importing the students from the csv file. Used in Memberinfo and GroupMapping
def ImportCsvFile(request, *args, **kwargs):
    if request.method == "POST" and request.FILES['import_csv']:
        media = request.FILES['import_csv']
        center_id = request.user.Center_Code.id
        file_name = uuid.uuid4()
        extension = media.name.split('.')[-1]
        new_file_name = str(file_name) + '.' + str(extension)
        path = 'media/import_csv/' + str(center_id)

        fs = FileSystemStorage(location=path)
        filename = fs.save(new_file_name + '.' + extension, media)
        path = os.path.join(path, filename)
        df = pd.read_csv(path, encoding='utf-8')  # delimiter=';|,', engine='python',
        df.column = ['Username', 'Member ID', 'First Name', 'Last Name', 'Email', 'Phone', 'Gender', 'Student',
                     'Teacher', 'Temporary Address', 'Permanent Address', 'Birthdate']
        # Drop empty row of excel csv file
        df = df.dropna(how='all')
        df = df.replace(pd.np.nan, '', regex=True)
        saved_id = []
        previous_uname = []
        for i in range(len(df)):
            try:

                obj_username = df.iloc[i]['Username']
                if MemberInfo.objects.filter(username__iexact=obj_username).exists():
                    previous_uname.append(obj_username)
                    continue
                
                obj = MemberInfo()
                obj.username = obj_username
                obj.Member_ID = df.iloc[i]['Member ID']
                obj.first_name = df.iloc[i]['First Name']
                obj.last_name = df.iloc[i]['Last Name']
                obj.email = df.iloc[i]['Email']
                obj.Member_Permanent_Address = df.iloc[i]['Permanent Address']
                obj.Member_Temporary_Address = df.iloc[i]['Temporary Address']
                try:
                    obj.Member_BirthDate = datetime.strptime(df.iloc[i]['Birthdate'], "%m/%d/%Y").strftime('%Y-%m-%d')
                except:
                    obj.Member_BirthDate = None
                obj.Member_Phone = df.iloc[i]['Phone']

                if df.iloc[i]['Gender'] == 'Male' or df.iloc[i]['Gender'] == 'M':
                    obj.Member_Gender = 'M'
                elif df.iloc[i]['Gender'] == 'Female' or df.iloc[i]['Gender'] == 'F':
                    obj.Member_Gender = 'F'
                else:
                    obj.Member_Gender = ''

                # This is to check if the url contains the query parameter groupmappingpk.
                # groupmappingpk is added to url when this function is called from groupmapping_detail.html.
                # If groupmappingpk is in the url then the csv file containing all members are students only.
                if request.GET.get('groupmappingpk'):
                    obj.Is_Student = True
                else:
                    if df.iloc[i]['Teacher'] == 1:
                        obj.Is_Teacher = True
                    else:
                        obj.Is_Teacher = False

                    if df.iloc[i]['Student'] == 1:
                        obj.Is_Student = True
                    else:
                        obj.Is_Student = False

                obj.Center_Code = request.user.Center_Code
                obj.set_password('00000')
                obj.save()

                # Following is to add the new students to the group from which they were imported.
                # groupmappingpk contains the primary key of the group that is used to call the function.
                if request.GET.get('groupmappingpk'):
                    # If no group exist then raise the exception to terminate the process
                    if GroupMapping.objects.filter(pk=request.GET.get('groupmappingpk')).exists():
                        g = GroupMapping.objects.get(pk=request.GET.get('groupmappingpk'))
                    else:
                        raise Exception('Group %s does not exist' % request.GET.get('groupmappingpk'))
                    obj.groupmapping_set.add(g)
                saved_id.append(obj.id)


            except Exception as e:
                for j in saved_id:
                    MemberInfo.objects.filter(id=j).delete()
                msg = "Can't Upload all data. Problem in " + str(
                    i + 1) + "th row of data while uploading. <br><br> " + "<br> ".join(
                    ["{} -> {}".format(k, v) for k, v in df.iloc[i].to_dict().items()]) + "<br><br>"
                return JsonResponse(data={"message": msg, "class": "text-danger", "rmclass": "text-success"})
        if previous_uname:
            messages = """User Data has been uploaded<br><div class='text-danger'>But These users are already
             present in the system so are not registered:<br>""" + str(previous_uname) + """</div>"""
        else:
            messages = "All data has been Uploaded Sucessfully"
        return JsonResponse(data={"message": messages, "class": "text-success",
                                  "rmclass": "text-danger"})


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('user_profile')
    template_name = 'registration/password_change_form.html'
    title = _('Password change')

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)

        messages.success(self.request,
                         'Your password was successfully updated! You can login with your new credentials')

        return super().form_valid(form)


class MemberInfoDetailView(MemberAuthMxnCls, DetailView):
    model = MemberInfo


class MemberInfoUpdateView(MemberAuthMxnCls, UpdateView):
    model = MemberInfo
    form_class = MemberUpdateForm


class MemberInfoDeleteView(MemberAuthMxnCls, DeleteView):
    model = MemberInfo
    success_url = reverse_lazy('memberinfo_list')

    def post(self, request, *args, **kwargs):
        redirect_link = self.request.POST.get('redirect', 'memberinfo_list')
        try:
            self.delete(request, *args, **kwargs)
            messages.success(request, "The user is deleted Successfully")
            return redirect(redirect_link)
        except:
            messages.error(request,
                           "You can't delete this user instead you can turn off the status value which will disable the user.")
            return redirect(redirect_link)


class CourseInfoListView(ListView):
    model = CourseInfo
    paginate_by = 6

    def get_queryset(self):
        qs = self.model.objects.filter(Center_Code=self.request.user.Center_Code)
        query = self.request.GET.get('query')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__icontains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs


class CourseInfoCreateView(AdminAuthMxnCls, CreateView):
    model = CourseInfo
    form_class = CourseInfoForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class CourseInfoDetailView(CourseAuthMxnCls, AdminAuthMxnCls, DetailView):
    model = CourseInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Quiz.objects.filter(course_code=self.kwargs.get('pk'), exam_paper=True,
                                                   chapter_code=None)  # exam type
        context['numberOfQuizExclExams'] = Quiz.objects.filter(
            chapter_code__in=context['chapters'].values_list('pk'),
            exam_paper=False, course_code=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.filter(course_associated_with=self.kwargs.get('pk'))
        context['exam_quiz'] = Quiz.objects.filter(exam_paper=True, course_code=self.object)
        return context


class CourseInfoUpdateView(CourseAuthMxnCls, AdminAuthMxnCls, UpdateView):
    model = CourseInfo
    form_class = CourseInfoForm

    def get_form_kwargs(self):
        """
        Returns the keyword arguments for instantiating the form.
        """
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


def CourseInfoDeleteView(request, pk):
    if request.method == 'POST':
        if AuthCheck(request, admn=1) == 2 or CourseAuth(request, pk) == 2:
            return redirect('login')
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = CourseInfo.objects.get(pk=pk)
            Obj.delete()
            return redirect('courseinfo_list')

        except:
            messages.error(request,
                           "Cannot delete courses if have any chapters, association with inning groups, survey, quiz or forum. Please make sure all associations with this chapters are deleted. ")
            return redirect('courseinfo_detail', pk=pk)


class ChapterInfoListView(ListView):
    model = ChapterInfo


class ChapterInfoCreateView(CreateView):
    model = ChapterInfo
    form_class = ChapterInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['datetime'] = datetime.now()
        return context


class ChapterInfoCreateViewAjax(AjaxableResponseMixin, CreateView):
    model = ChapterInfo
    form_class = ChapterInfoForm
    template_name = 'ajax/chapterinfo_form_ajax.html'

    # def post(self, request, *args, **kwargs):
    #     Obj = ChapterInfo()
    #     Obj.Chapter_No = request.POST["Chapter_No"]
    #     Obj.Chapter_Name = request.POST["Chapter_Name"]
    #     Obj.Summary = request.POST["Summary"]
    #     if request.POST["Use_Flag"] == 'false':
    #         Obj.Use_Flag = False
    #     else:
    #         Obj.Use_Flag = True
    #     Obj.mustreadtime = int(request.POST['mustreadtime']) * 60
    #     Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
    #     Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
    #     Obj.save()

    #     return JsonResponse(
    #         data={'Message': 'Success'}
    #     )

    def form_valid(self, form):
        form.save(commit=False)
        if form.cleaned_data['Start_Date'] == "":
            form.instance.Start_Date = None
        if form.cleaned_data['End_Date'] == "":
            form.instance.End_Date = None
        form.save()
        return JsonResponse(
            data={'Message': 'Success'}
        )

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors}, status=500)


class ChapterInfoDetailView(AdminAuthMxnCls, ChapterAuthMxnCls, DetailView):
    model = ChapterInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(ChapterInfo, Course_Code=self.kwargs.get('course'),
                                              pk=self.kwargs.get('pk'))
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        context['post_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), post_test=True)
        context['pre_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), pre_test=True)
        context['datetime'] = datetime.now()
        return context


class ChapterInfoDeleteView(ChapterAuthMxnCls, DeleteView):
    model = ChapterInfo

    def post(self, request, *args, **kwargs):
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = ChapterInfo.objects.get(pk=request.POST['chapter_id'])
            Obj.delete()
            return redirect('courseinfo_detail', pk=request.POST['course_id'])

        except:
            messages.error(request,
                           "Cannot delete chapter with assignments")
            return redirect('chapterinfo_detail', course=self.request.POST['course_id'],
                            pk=self.request.POST['chapter_id'])


def CourseForum(request, course):
    course = CourseInfo.objects.get(pk=course)
    course_forum = None
    course_node_forum = None
    try:
        course_node_forum = NodeGroup.objects.get(title='Course')
    except ObjectDoesNotExist:
        NodeGroup.objects.create(title='Course', description='Root node for course Forum').save()
        course_node_forum = NodeGroup.objects.get(title='Course')

    try:
        course_forum = Topic.objects.get(course_associated_with=course)
    except ObjectDoesNotExist:
        Topic.objects.create(title=course.Course_Name, node_group=course_node_forum, course_associated_with=course,
                             center_associated_with=request.user.Center_Code, topic_icon="book").save()
        course_forum = Topic.objects.get(course_associated_with=course)

    return redirect('forum:topic', pk=course_forum.pk)


class ChapterInfoUpdateView(ChapterAuthMxnCls, UpdateView):
    model = ChapterInfo
    form_class = ChapterInfoForm

    def form_valid(self, form):
        form.save(commit=False)
        if form.cleaned_data['Start_Date'] == "":
            form.instance.Start_Date = None
        if form.cleaned_data['End_Date'] == "":
            form.instance.End_Date = None

        form.instance.mustreadtime = int(form.cleaned_data['mustreadtime']) * 60
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        return context


class SessionInfoCreateViewPopup(CreateView):
    model = SessionInfo
    form_class = SessionInfoForm
    template_name = 'popup/sessioninfoformpopup.html'


class InningGroupCreateViewPopup(CreateView):
    model = SessionInfo
    form_class = SessionInfoForm
    template_name = 'popup/inninggroupformpopup.html'


class GroupMappingCreateViewPopup(CreateView):
    model = SessionInfo
    form_class = SessionInfoForm
    template_name = 'popup/groupmappingformpopup.html'


class SessionInfoListView(ListView):
    model = SessionInfo

    # Send data only related to the center
    def get_queryset(self):
        return SessionInfo.objects.filter(Center_Code=self.request.user.Center_Code)


class SessionInfoCreateView(CreateView):
    model = SessionInfo
    form_class = SessionInfoForm


class SessionInfoDetailView(DetailView):
    model = SessionInfo


class SessionInfoUpdateView(UpdateView):
    model = SessionInfo
    form_class = SessionInfoForm


class InningInfoListView(ListView):
    model = InningInfo
    template_name = 'WebApp/inninginfo_list.html'

    def get_queryset(self):
        return InningInfo.objects.filter(Center_Code=self.request.user.Center_Code, End_Date__gte=datetime.now())


class InningInfoListViewInactive(ListView):
    model = InningInfo
    template_name = 'WebApp/inninginfo_list_inactive.html'

    def get_queryset(self):
        return InningInfo.objects.filter(Center_Code=self.request.user.Center_Code, End_Date__lte=datetime.now())


class InningInfoCreateView(CreateView):
    model = InningInfo
    form_class = InningInfoForm

    def get_form_kwargs(self):
        kwargs = super(InningInfoCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(InningInfoCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        if 'saveasnew' in self.request.path:
            inning = get_object_or_404(InningInfo, pk=self.kwargs['pk'])
            initial['Inning_Name'] = inning.Inning_Name
            initial['Groups'] = inning.Groups
            initial['Course_Group'] = inning.Course_Group.all()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.now()
        context['base_file'] = 'base.html'
        return context


class InningInfoDetailView(InningInfoAuthMxnCls, DetailView):
    model = InningInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['SessionSurvey'] = SurveyInfo.objects.filter(Session_Code=self.kwargs['pk'])
        if InningManager.objects.filter(sessioninfoobj__pk=self.kwargs['pk']).exists():
            context['session_managers'] = get_object_or_404(InningManager, sessioninfoobj__pk=self.kwargs['pk'])
        return context


class InningInfoUpdateView(InningInfoAuthMxnCls, UpdateView):
    model = InningInfo
    form_class = InningInfoForm

    def get_form_kwargs(self):
        kwargs = super(InningInfoUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.now()
        context['base_file'] = 'base.html'
        return context


def InningInfoDeleteView(request, pk):
    if request.method == 'POST':
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = InningInfo.objects.get(pk=pk)
            Obj.delete()
            return redirect('inninginfo_list')

        except:
            messages.error(request,
                           "Cannot delete inning")
            return redirect('inninginfo_detail', pk=pk)


class InningGroupListView(ListView):
    model = InningGroup

    # Send data only related to the center
    def get_queryset(self):
        return InningGroup.objects.filter(Center_Code=self.request.user.Center_Code)


class InningGroupCreateView(CreateView):
    model = InningGroup
    form_class = InningGroupForm

    def get_form_kwargs(self):
        kwargs = super(InningGroupCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "base.html"
        return context


class InningGroupCreateAjax(AjaxableResponseMixin, CreateView):
    model = InningGroup
    form_class = InningGroupForm
    template_name = 'ajax/inninggroup_form_ajax.html'

    def get_form_kwargs(self):
        kwargs = super(InningGroupCreateAjax, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class InningInfoCreateSessionAjax(AjaxableResponseMixin, CreateView):
    model = SessionInfo
    form_class = SessionInfoForm
    template_name = 'ajax/sessioncreate_form_ajax.html'


class InningGroupDetailView(InningGroupAuthMxnCls, DetailView):
    model = InningGroup


class InningGroupUpdateView(InningGroupAuthMxnCls, UpdateView):
    model = InningGroup
    form_class = InningGroupForm

    def form_valid(self, form):
        """If the form is valid, redirect to the supplied URL."""
        messages.add_message(self.request, messages.SUCCESS, 'Course Teacher Allocation Updated.')
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "base.html"
        return context

    def get_form_kwargs(self):
        kwargs = super(InningGroupUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


def InningGroupDeleteView(request, pk):
    if request.method == 'POST':
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = InningGroup.objects.get(pk=pk)
            Obj.delete()
            return redirect('inninggroup_list')

        except:
            messages.error(request,
                           "Cannot delete Teacher Allocation")
            return redirect('inninggroup_detail', pk=pk)


class GroupCreateSessionAjax(AjaxableResponseMixin, CreateView):
    model = GroupMapping
    form_class = GroupMappingForm
    template_name = 'ajax/groupcreate_form_ajax.html'

    def get_form_kwargs(self):
        kwargs = super(GroupCreateSessionAjax, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class GroupMappingListView(ListView):
    model = GroupMapping

    # Send data only related to the center
    def get_queryset(self):
        return GroupMapping.objects.filter(Center_Code=self.request.user.Center_Code)


def GroupMappingCSVImport(request, *args, **kwargs):
    if request.method == "POST" and request.FILES['import_csv']:
        media = request.FILES['import_csv']
        center_id = request.user.Center_Code.id
        file_name = uuid.uuid4()
        extension = media.name.split('.')[-1]
        new_file_name = str(file_name) + '.' + str(extension)
        path = 'media/import_csv/student_group' + str(center_id)

        fs = FileSystemStorage(location=path)
        filename = fs.save(new_file_name + '.' + extension, media)
        path = os.path.join(path, filename)
        df = pd.read_csv(path, encoding='utf-8')  # delimiter=';|,', engine='python',
        df = df.dropna(how='all')

        reg_agent = request.user.username
        center = request.user.Center_Code
        err_msg = []
        msg = []
        try:
            groups = df['Group'].unique()
        except Exception as e:
            return JsonResponse(
                data={"message": "There is no Column <b>Group</b> in the input file", "class": "text-danger",
                      "rmclass": "text-success"})
        for i in range(len(groups)):
            try:
                flag = 0
                obj = GroupMapping()
                obj.GroupMapping_Name = groups[i]
                obj.Register_Agent = reg_agent
                obj.Center_Code = center
                students = df[df['Group'] == groups[i]].reset_index(drop=True)
                obj.save()
                for j in range(len(students)):
                    if MemberInfo.objects.filter(username=students['Username'][j]).exists():
                        obj_student = MemberInfo.objects.get(username=students['Username'][j])
                        obj.Students.add(obj_student)
                    else:
                        # obj_create = MemberInfo()
                        # obj_create.username = students['Username'][j]
                        # obj_create.Center_Code = center
                        # obj_create.save()
                        # obj.Students.add(obj_student)
                        err_msg.append(
                            "Student Group: <b>{}</b> can't be created: Student- <b>{}</b> not found<br>".format(
                                groups[i], students['Username'][j]))
                        flag = 1
                        break

                if flag == 1:
                    obj.delete()
                    if msg:
                        err_msg = err_msg + msg
                        msg.clear()
                else:
                    msg.append("<div class='text-success'>Student Group: <b>{}</b> created</div>".format(groups[i]))
                    if err_msg:
                        err_msg = err_msg + msg
                        msg.clear()
            except Exception as e:
                err_msg.append("Student Group: <b>{}</b> can't be created<br> {}".format(groups[i], e))
    if err_msg:
        return JsonResponse(data={"message": err_msg, "class": "text-danger", "rmclass": "text-success"})
    return JsonResponse(data={"message": msg, "class": "text-success", "rmclass": "text-danger"})


class GroupMappingCreateView(CreateView):
    model = GroupMapping
    form_class = GroupMappingForm

    def get_form_kwargs(self):
        kwargs = super(GroupMappingCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(GroupMappingCreateView, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        if 'saveasnew' in self.request.path:
            initial['Students'] = get_object_or_404(GroupMapping, pk=self.kwargs['pk']).Students.all()
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "base.html"
        return context


class GroupMappingDetailView(GroupMappingAuthMxnCls, DetailView):
    model = GroupMapping


class GroupMappingUpdateView(GroupMappingAuthMxnCls, UpdateView):
    model = GroupMapping
    form_class = GroupMappingForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['base_file'] = "base.html"
        return context

    def get_form_kwargs(self):
        kwargs = super(GroupMappingUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


def GroupMappingDeleteView(request, pk):
    if request.method == 'POST':
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = GroupMapping.objects.get(pk=pk)
            Obj.delete()
            return redirect('groupmapping_list')

        except:
            messages.error(request,
                           "Cannot delete Group Mapping")
            return redirect('groupmapping_detail', pk=pk)


# AssignmentInfoViews
class AssignmentInfoListView(ListView):
    model = AssignmentInfo


class AssignmentInfoCreateView(CreateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        return context


class AssignmentInfoCreateViewAjax(AjaxableResponseMixin, CreateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm
    template_name = 'ajax/assignmentinfo_form_ajax.html'

    def post(self, request, *args, **kwargs):
        Obj = AssignmentInfo()
        Obj.Assignment_Topic = request.POST["Assignment_Topic"]
        Obj.Assignment_Start = request.POST["Assignment_Start"]
        Obj.Assignment_Deadline = request.POST["Assignment_Deadline"]
        Obj.Use_Flag = request.POST["Use_Flag"].capitalize()
        Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
        Obj.Chapter_Code = ChapterInfo.objects.get(id=request.POST["Chapter_Code"])
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])

        if Obj.Assignment_Start and Obj.Assignment_Deadline:
            if (Obj.Assignment_Start > Obj.Assignment_Deadline):
                return JsonResponse(
                    data={'Message': 'Assignment Deadline must be greater than start date.'}, status=500
                )
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


class AssignmentInfoEditViewAjax(AjaxableResponseMixin, CreateView):
    model = AssignmentInfo

    def post(self, request, *args, **kwargs):
        try:
            Obj = AssignmentInfo.objects.get(pk=request.POST["Assignment_ID"])
            Obj.Assignment_Topic = request.POST["Assignment_Topic"]
            Obj.Assignment_Start = request.POST["Assignment_Start"]
            Obj.Assignment_Deadline = request.POST["Assignment_Deadline"]
            Obj.Use_Flag = request.POST["Use_Flag"].capitalize()
            Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
            Obj.Chapter_Code = ChapterInfo.objects.get(id=request.POST["Chapter_Code"])
            Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
            if Obj.Assignment_Start and Obj.Assignment_Deadline:
                if (Obj.Assignment_Start > Obj.Assignment_Deadline):
                    return JsonResponse(
                        data={'Message': 'Deadline date must be greater than start date'},
                        status=500
                    )
            Obj.save()

            return JsonResponse(
                data={'Message': 'Success'}
            )

        except:
            return JsonResponse(
                data={'Message': 'Fail'}
            )


class AssignmentInfoDetailView(AssignmentInfoAuthMxnCls, DetailView):
    model = AssignmentInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['datetime'] = datetime.now()
        return context


class AssignmentInfoUpdateView(AssignmentInfoAuthMxnCls, UpdateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        return context


class AssignmentInfoDeleteView(DeleteView):
    model = AssignmentInfo

    def post(self, request, *args, **kwargs):

        try:
            # return self.delete(request, *args, **kwargs)
            Obj = AssignmentInfo.objects.get(pk=self.request.POST['assignment_id'])
            Obj.delete()
            return redirect('chapterinfo_detail', course=request.POST['course_id'], pk=request.POST['chapter_id'])

        except:
            messages.error(request,
                           "Cannot delete assignment")
            return redirect('assignmentinfo_detail', course=self.request.POST['course_id'],
                            chapter=self.request.POST['chapter_id'], pk=self.request.POST['assignment_id'])


class QuestionInfoListView(ListView):
    model = AssignmentQuestionInfo


class QuestionInfoCreateView(CreateView):
    model = AssignmentQuestionInfo
    form_class = QuestionInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class QuestionInfoCreateViewAjax(AjaxableResponseMixin, CreateView):
    model = AssignmentQuestionInfo
    form_class = QuestionInfoForm
    template_name = 'ajax/questioninfo_form_ajax.html'

    def post(self, request, *args, **kwargs):
        Obj = AssignmentQuestionInfo()
        Obj.Question_Title = request.POST["Question_Title"]
        Obj.Question_Score = request.POST["Question_Score"]
        Obj.Question_Description = request.POST["Question_Description"]
        Obj.Answer_Type = request.POST["Answer_Type"]
        if request.POST["Use_Flag"] == 'true':
            Obj.Use_Flag = True
        else:
            Obj.Use_Flag = False
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
        Obj.Assignment_Code = AssignmentInfo.objects.get(pk=request.POST["Assignment_Code"])
        if bool(request.FILES.get('Question_Media_File', False)) == True:
            media = request.FILES['Question_Media_File']
            if media.size / 1024 > 2048:
                return JsonResponse(data={'status': 'Fail', "msg": "File size exceeds 2MB"}, status=500)
            path = settings.MEDIA_ROOT
            name = (str(uuid.uuid4())).replace('-', '') + '.' + media.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/Question_Media_Files/')
            filename = fs.save(name, media)
            Obj.Question_Media_File = 'Question_Media_Files/' + name
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


class QuestionInfoEditViewAjax(AjaxableResponseMixin, CreateView):
    model = AssignmentQuestionInfo

    def post(self, request, *args, **kwargs):
        try:
            Obj = AssignmentQuestionInfo.objects.get(pk=request.POST["pk"])
            Obj.Question_Title = request.POST["Question_Title"]
            Obj.Question_Score = request.POST["Question_Score"]
            Obj.Question_Description = request.POST["Question_Description"]
            Obj.Answer_Type = request.POST["Answer_Type"]
            if request.POST["Use_Flag"] == 'true':
                Obj.Use_Flag = True
            else:
                Obj.Use_Flag = False

            Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
            Obj.Assignment_Code = AssignmentInfo.objects.get(pk=request.POST["Assignment_Code"])
            if request.POST["clear"] == 'true':
                Obj.Question_Media_File = ''
            else:
                if bool(request.FILES.get('Question_Media_File', False)) == True:
                    media = request.FILES['Question_Media_File']
                    if media.size / 1024 > 2048:
                        return JsonResponse(data={'status': 'Fail', "msg": "File size exceeds 2MB"}, status=500)
                    path = settings.MEDIA_ROOT
                    name = (str(uuid.uuid4())).replace('-', '') + '.' + media.name.split('.')[-1]
                    fs = FileSystemStorage(location=path + '/Question_Media_Files/')
                    filename = fs.save(name, media)
                    Obj.Question_Media_File = 'Question_Media_Files/' + name
            Obj.save()

        except:
            return JsonResponse(
                data={'Message': 'Cannot edit form'}
            )
        return JsonResponse(
            data={'Message': 'Success'}
        )


class QuestionInfoDetailView(DetailView):
    model = AssignmentQuestionInfo


class QuestionInfoUpdateView(UpdateView):
    model = AssignmentQuestionInfo
    form_class = QuestionInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class QuestionInfoDeleteView(DeleteView):
    model = AssignmentQuestionInfo

    def post(self, request, *args, **kwargs):

        try:
            # return self.delete(request, *args, **kwargs)
            Obj = AssignmentQuestionInfo.objects.get(pk=self.request.POST['question_id'])
            Obj.delete()
            return redirect('assignmentinfo_detail', course=request.POST['course_id'],
                            chapter=request.POST['chapter_id'], pk=request.POST['assignment_id'])

        except:
            messages.error(request,
                           "Cannot delete question")
            return redirect('assignmentinfo_detail', course=request.POST['course_id'],
                            chapter=request.POST['chapter_id'], pk=request.POST['assignment_id'])


class AssignAssignmentInfoListView(ListView):
    model = AssignAssignmentInfo


class AssignAssignmentInfoCreateView(CreateView):
    model = AssignAssignmentInfo
    form_class = AssignAssignmentInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Inning_Code'] = get_object_or_404(InningInfo, pk=self.kwargs.get('session'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class AssignAssignmentInfoDetailView(DetailView):
    model = AssignAssignmentInfo


class AssignAssignmentInfoUpdateView(UpdateView):
    model = AssignAssignmentInfo
    form_class = AssignAssignmentInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Inning_Code'] = get_object_or_404(InningInfo, pk=self.kwargs.get('session'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class AssignAnswerInfoListView(ListView):
    model = AssignAnswerInfo


class AssignAnswerInfoCreateView(CreateView):
    model = AssignAnswerInfo
    form_class = AssignAnswerInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Question_Code'] = get_object_or_404(AssignmentQuestionInfo, pk=self.kwargs.get('questioncode'))
        return context


class AssignAnswerInfoDetailView(DetailView):
    model = AssignAnswerInfo


def AssignAnswerInfoDelete(request):
    if request.method == "POST":
        answerpk = request.POST.get('answerpk')
        if AssignAnswerInfo.objects.filter(pk=answerpk).exists():
            AssignAnswerInfo.objects.get(pk=answerpk).delete()
            messages.add_message(request, messages.SUCCESS, 'Deleted successfully')
            return HttpResponse('success', status=200)
        else:
            messages.add_message(request, messages.ERROR, 'Answer doesn\'t exist')
            return HttpResponse('Answer doesn\'t exist', status=404)
    else:
        messages.add_message(request, messages.ERROR, 'Invalid')
        return HttpResponse('GET Method not allowed', status=403)


class AssignAnswerInfoUpdateView(UpdateView):
    model = AssignAnswerInfo
    form_class = AssignAnswerInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Question_Code'] = get_object_or_404(AssignmentQuestionInfo, pk=self.kwargs.get('questioncode'))
        return context


def question(request):
    return render(request, 'WebApp/question.html')


def polls(request):
    return render(request, 'WebApp/polls.html')


class MessageInfoListView(ListView):
    model = MessageInfo


class MessageInfoCreateView(CreateView):
    model = MessageInfo
    form_class = MessageInfoForm


class MessageInfoDetailView(DetailView):
    model = MessageInfo


class MessageInfoUpdateView(UpdateView):
    model = MessageInfo
    form_class = MessageInfoForm


# chapter builder code starts from here

def make_directory_if_not_exists(courseID, chapterID):
    path = settings.MEDIA_ROOT
    # following is commented because filesystemstorage auto create directories if not exist
    if not os.path.exists(os.path.join(path, 'chapterBuilder')):
        os.makedirs(os.path.join(path, 'chapterBuilder'))
    if not os.path.exists(path + '/chapterBuilder/' + courseID):
        print(path + '/chapterBuilder/' + courseID)
        os.makedirs(os.path.join(path, 'chapterBuilder/' + courseID))
    if not os.path.exists(path + '/chapterBuilder/' + courseID + '/' + chapterID):
        os.makedirs(os.path.join(path, 'chapterBuilder/' + courseID + '/' + chapterID))


def chapterviewer(request):
    if request.method == "GET":
        path = settings.MEDIA_ROOT
        chapterID = request.GET['chapterID']
        chapterobj = ChapterInfo.objects.get(id=chapterID)
        courseID = chapterobj.Course_Code.id
        file_path = path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(chapterID) + '.txt'

        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            data = 1
        else:
            data = 0
        return JsonResponse({'data': data})


def chapterpagebuilder(request, course, chapter):
    chapterlist = ChapterInfo.objects.filter(Course_Code=CourseInfo.objects.get(id=course))
    chapterdetails = chapterlist.get(id=chapter)
    path = settings.MEDIA_ROOT
    server_name = settings.SERVER_NAME
    data = {"": ""}
    try:
        with open(path + '/chapterBuilder/' + str(course) + '/' + str(chapter) + '/' + str(
                chapter) + '.txt') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(e)
    context = {
        'course': course,
        'chapter': chapter,
        'chapterdetails': chapterdetails,
        'chapterlist': chapterlist,
        'file_path': path,
        'server_name': server_name,
        'data': data
    }
    return render(request, 'WebApp/chapterbuilder.html', context)


def save_file(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        media_type = request.POST['type']
        path = ''
        if request.FILES['file-0']:
            media = request.FILES['file-0']
            if media_type == 'pic':
                if (media.size / 1024) > 2048:
                    return JsonResponse(data={"message": "File size exceeds 2MB"}, status=500)
            path = settings.MEDIA_ROOT

            # file name for the saved file --> uuid&&&uploadedfilename&&&userPK
            # Eg: 561561561&&&test.jpg&&&17
            name = (str(uuid.uuid4())).replace('-', '') + '___' + "".join(
                re.findall("[a-zA-Z0-9]+", media.name.split('.')[0])) + '___' + str(
                request.user.pk) + '.' + media.name.split('.')[-1]
            # name = "".join(re.findall("[a-zA-Z0-9]+", name))
            fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            filename = fs.save(name, media)

        return JsonResponse(data={"message": "success", "media_name": name})


def newChapterBuilder(request, course, chapter):
    chapterlist = ChapterInfo.objects.filter(Course_Code=CourseInfo.objects.get(id=course))
    chapterdetails = chapterlist.get(id=chapter)
    path = settings.MEDIA_ROOT
    server_name = settings.SERVER_NAME
    data = {"": ""}
    try:
        with open(path + '/chapterBuilder/' + str(course) + '/' + str(chapter) + '/' + str(
                chapter) + '.txt') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(e)
    context = {
        'course': course,
        'chapter': chapter,
        'chapterdetails': chapterdetails,
        'chapterlist': chapterlist,
        'file_path': path,
        'server_name': server_name,
        'data': data
    }
    return render(request, "WebApp/newChapterBuilder.html", context)


def deletechapterfile(request):
    if request.method == 'POST' and request.user.is_authenticated:
        old_file = json.loads(request.POST['old'])
        for key, value in old_file.items():
            for x in value:
                if key == '_3d':
                    if os.path.exists(os.path.join(BASE_DIR, x[10:])):
                        extensions = ['mtl', 'obj']
                        for ext in extensions:
                            if os.path.exists(os.path.join(BASE_DIR, x[10:-4] + '.' + ext)):
                                os.remove(os.path.join(BASE_DIR, x[10:-4] + '.' + ext))
                        return JsonResponse({'message': 'deletion success'})
                if os.path.exists(os.path.join(BASE_DIR, x[1:])):
                    os.remove(os.path.join(BASE_DIR, x[1:]))
                    return JsonResponse({'message': 'deletion success'})
    return HttpResponse('')


def save_3d_file(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        path = ''
        if request.FILES['objfile']:
            obj = request.FILES['objfile']
            # try:
            #     mtl = request.FILES['mtlfile']
            # except:
            #     mtl = None
            path = settings.MEDIA_ROOT

            # file name for the saved file --> uuid&&&uploadedfilename&&&userPK
            # Eg: 561561561&&&test.jpg&&&17
            name = (str(uuid.uuid4())).replace('-', '') + '___' + "".join(
                re.findall("[a-zA-Z0-9]+", obj.name.split('.')[0])) + '___' + str(
                request.user.pk)
            # name = "".join(re.findall("[a-zA-Z]+", name))
            objname = name + '.' + obj.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            filename = fs.save(objname, obj)
            # if mtl is not None:
            #     mtlname = name + '.' + mtl.name.split('.')[-1]
            #     fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            #     filename = fs.save(mtlname, mtl)
        return JsonResponse(data={"message": "success", "objname": objname})


def save_video(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        media_type = request.POST['type']
        path = ''
        if request.FILES['file-0']:
            media = request.FILES['file-0']
            if (media.size / 1024) > (2048 * 1024):  # checking if file size is greater than 2 GB
                return JsonResponse(data={"message": "File size exceeds 2GB"}, status=500)

        path = settings.MEDIA_ROOT

        # file name for the saved file --> uuid&&&uploadedfilename&&&userPK
        # Eg: 561561561&&&test.jpg&&&17
        name = (str(uuid.uuid4())).replace('-', '') + '___' + "".join(
            re.findall("[a-zA-Z0-9]+", media.name.split('.')[0])) + '___' + str(
            request.user.pk) + '.' + media.name.split('.')[-1]

        # fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
        # filename = fs.save(name, media)
        # return JsonResponse({'media_name': name})
        # video uploading to vimeo.com

        # Premium Account
        # v = vimeo.VimeoClient(
        #     token='3b42ecf73e2a1d0088dd677089d23e32',
        #     key='3b55a8ee9a7d0702c787c18907e79ceaa535b0e3',
        #     secret='KU1y3Bl/ZWj3ZgEzi7g5dtr8bESaBkqBtH5np1QUKBI0zLDvxteNURzRW09kl6QXqKLnCjtV15r0VwV+9nsYu6GmNFw5vjb4zKDWqpsWT+qPBn2I23n+ckLglgIvHmBh'
        # )

        data = {
            "upload": {
                "approach": "tus",
                "size": media.size
            },
            'name': name
        }
        rs = requests.session()

        # if getServerIP() != '103.41.247.44':  # 103.41.247.44 is ip of ublcloud.me (indonesian). If request if for ublcloud, then it will save to server else to vimeo
        if settings.SERVER_NAME != 'Indonesian_Server':
            r = rs.post(url="https://api.vimeo.com/me/videos",
                        headers={'Authorization': 'bearer 3b42ecf73e2a1d0088dd677089d23e32',
                                 'Content-Type': 'application/json',
                                 'Accept': 'application/vnd.vimeo.*+json;version=3.4'},
                        data=json.dumps(data))
            if r.status_code == 200:
                r_responseText = json.loads(r.text)
                res = rs.patch(r_responseText['upload']['upload_link'], headers={'Tus-Resumable': '1.0.0',
                                                                                 'Content-Type': 'application/offset+octet-stream',
                                                                                 'Accept': 'application/vnd.vimeo.*+json;version=3.4',
                                                                                 'Connection': 'keep-alive',
                                                                                 'Upload-Offset': '0'},
                               data=media.file
                               )

                if res.status_code == 204 or res.status_code == 200:
                    response = rs.head(r_responseText['upload']['upload_link'])

                    a = rs.put(
                        url='https://api.vimeo.com/me/projects/1508982/videos/' + r_responseText['uri'].split('/')[-1],
                        headers={'Authorization': 'bearer 3b42ecf73e2a1d0088dd677089d23e32',
                                 'Content-Type': 'application/json',
                                 'Accept': 'application/vnd.vimeo.*+json;version=3.4'}, ),
                    return JsonResponse(
                        {'link': r_responseText['upload']['upload_link'], 'media_name': name,
                         'html': r_responseText['embed']['html']})
        else:
            if (media.size / 1024) > (500 * 1024):  # checking if file size is greater than 500 MB in Indonesian Server
                return JsonResponse(data={"message": "File size exceeds 500 MB"}, status=500)
            if media.name.split('.')[-1] != 'mp4' and (media.size / 1024) > (
                    100 * 1024):  # if media size is 100 MB and media is not mp4
                return JsonResponse(data={"message": "File size above 100 MB must be MP4"}, status=500)

            name = (str(uuid.uuid4())).replace('-', '') + '' + "".join(
                re.findall("[a-zA-Z0-9]+", media.name.split('.')[0])) + '' + str(
                request.user.pk)
            cloudinary.config(
                cloud_name="nsdevil-com",
                api_key="355159163645263",
                api_secret="riH4CD94zuSXffS_wfSgIFgxmJ0"
            )
            response = cloudinary.uploader.upload_large(media.file,
                                                        folder="/id.ublcloud.me",
                                                        resource_type="video",
                                                        chunk_size=6000000,  # chunk size default is 6 MB
                                                        public_id=name,
                                                        )
            embedd_code = '<iframe src="' + response['secure_url'] + '"><video controls preload="none"><source src="' + \
                          response['secure_url'] + '" type="video/mp4" autostart="false"></video></iframe>'
            print(response)

            return JsonResponse(
                {'link': response['secure_url'], 'media_name': response['public_id'],
                 # 'html': embedd_code
                 })
            # fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            # filename = fs.save(name, media)
        return JsonResponse({}, status=500)


def save_json(request):
    if request.method == "POST":
        jsondata = json.loads(request.POST['json'])
        # htmldata = json.loads(request.POST['htmlfile'])
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        path = settings.MEDIA_ROOT

        # creates directory structure if not exists
        make_directory_if_not_exists(courseID, chapterID)

        # for saving json data for viewing purposes
        with open(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + chapterID + '.txt', 'w') as outfile:
            json.dump(jsondata, outfile, indent=4)

        # # for saving all html data of page for API purposes
        # with open(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + chapterID + 'html.txt',
        #           'w') as outfile:
        #     json.dump(htmldata, outfile, indent=4)

        chapterObj = ChapterInfo.objects.get(id=chapterID)
        chapterObj.Page_Num = int(jsondata['numberofpages'])
        chapterObj.save()

        return JsonResponse(data={"message": "Json Saved"})


def export_chapter(request, course, chapter):
    obj = CourseInfo.objects.get(id=course)
    coursename = obj.Course_Name
    path = settings.MEDIA_ROOT
    dir_name = path + '/chapterBuilder/' + str(course) + '/' + str(chapter)
    if not os.path.exists(dir_name):
        return HttpResponse('No directory')
    zipfile = shutil.make_archive(
        path + '/export/' + str(coursename) + '_Chapter' + str(chapter) + '_' + str(obj.pk) + '_' + str(chapter) + '_',
        'zip', dir_name)

    return redirect(
        settings.MEDIA_URL + '/export/' + str(coursename) + '_Chapter' + str(chapter) + '_' + str(obj.pk) + '_' + str(
            chapter) + '_' + '.zip')


def import_chapter(request):
    chapterID = request.POST['chapterID']
    courseID = request.POST['courseID']
    if request.FILES['filename']:
        filename = request.FILES['filename']
    if not filename.name.endswith('.zip'):
        return JsonResponse({'status': 'false', 'message': "Only zip files are allowed"}, status=500)
    zip = zipfile.ZipFile(filename)
    checkflag = False
    for file in zip.namelist():
        # print(zip.getinfo(file).filename) #gives content of file like 'ls' or 'dir'
        if zip.getinfo(file).filename.endswith('.txt'):
            checkflag = True
    if not checkflag:
        return JsonResponse({'status': 'false', 'message': "Not valid zip"}, status=500)

    path = settings.MEDIA_ROOT

    # creates directory structure if not exists
    make_directory_if_not_exists(courseID, chapterID)

    storage_path = path + '/chapterBuilder/' + courseID + '/' + chapterID + '/'
    for file in zip.namelist():
        if zip.getinfo(file).filename.endswith('.txt') and 'html' not in zip.getinfo(file).filename:
            with zip.open(zip.getinfo(file).filename) as json_file:
                my_json = json_file.read().decode('utf8')

                data = json.loads(my_json)

                if not all(k in data for k in ("numberofpages", "pages")):
                    return JsonResponse({'status': 'false', 'message': "Not valid zip"}, status=500)
                elif data['numberofpages'] is 0:
                    return JsonResponse({'status': 'false', 'message': "Not valid zip"}, status=500)

                # check if numberofpages and pages are in the dictionary or not

            continue
        zip.extract(file, storage_path)  # extract the file to current folder if it is a text file

    for u, v in data['pages'].items():
        for x in v:
            for (div, values) in x.items():
                if div == 'pic':
                    for value in range(len(values)):
                        for i, j in values[value].items():
                            if i == 'background-image':
                                p = (j.split('/'))
                                p[3], p[4] = courseID, chapterID
                                j = '/'.join(p)
                                data['pages'][u][0][div][value]['background-image'] = j
                if div == 'video':
                    for value in range(len(values)):
                        for i, j in values[value].items():
                            if i == 'local_link':
                                p = (j.split('/'))
                                p[3], p[4] = courseID, chapterID
                                j = '/'.join(p)
                                data['pages'][u][0][div][value]['local_link'] = j
                if div == '_3d':
                    for value in range(len(values)):
                        for i, j in values[value].items():
                            if i == 'link':
                                p = (j.split('/'))
                                p[3], p[4] = courseID, chapterID
                                j = '/'.join(p)
                                data['pages'][u][0][div][value]['link'] = j
                if div == 'pdf':
                    for value in range(len(values)):
                        for i, j in values[value].items():
                            if i == 'link':
                                p = (j.split('/'))
                                p[3], p[4] = courseID, chapterID
                                j = '/'.join(p)
                                data['pages'][u][0][div][value]['link'] = j
                if div == 'quizdiv':
                    for value in range(len(values)):
                        data['pages'][u][0][div][value]['quiz_btn_name'] = "Create Quiz"
                        try:
                            data['pages'][u][0][div][value].pop('link')
                        except Exception as e:
                            print(e)

                if div == 'surveydiv':
                    for value in range(len(values)):
                        data['pages'][u][0][div][value]['survey_btn_name'] = "Create Survey"
                        try:
                            data['pages'][u][0][div][value].pop('link')
                        except Exception as e:
                            print(e)
    return JsonResponse(data)
    # -------------------------------------------------------------------------------------------------------


def retrievechapterfile(request):
    chapterID = request.GET['chapterID']
    courseID = request.GET['courseID']
    userID = request.GET['userpk']
    path = settings.MEDIA_ROOT
    image_extensions = ['.jpg', '.png', '.jpeg', 'svg']
    video_extensions = ['.mp4', ]
    images = []
    videos = []
    pdf = []
    try:
        if os.path.exists(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID)):
            chapterfiles = os.listdir(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID))
            for files in chapterfiles:
                if (files[-4:] in image_extensions):
                    images.append(files)
                elif (files[-4:] in video_extensions):
                    videos.append(files)
                elif (files.endswith('.pdf')):
                    pdf.append(files)
        else:
            print("No directory of this chapter")
    except Exception as e:
        print(e)
    return JsonResponse({
        'images': images,
        'videos': videos,
        'pdf': pdf
    })


@xframe_options_exempt
def ThreeDViewer(request, urlpath=None):
    print(urlpath, "urlpath")
    mtlurlpath = None

    if not urlpath:
        urlpath = "static/3D_Viewer/Sample.obj"
        mtlurlpath = "static/3D_Viewer/Sample.mtl"
    else:
        mtlpath_expected = BASE_DIR + "/" + urlpath[:-4] + ".mtl"
        print("got it mtlpath_expected", mtlpath_expected)
        if os.path.isfile(mtlpath_expected):
            print("file exist ", mtlpath_expected, " url is:", mtlurlpath)
            mtlurlpath = (urlpath[:-4] if urlpath else '') + ".mtl"
        else:
            print("MTL doesnt exist", mtlpath_expected)
            mtlurlpath = "static/3D_Viewer/none.mtl"

    return render(request, '3D_Viewer/render_template.html', {'objpath': urlpath, 'mtlpath': mtlurlpath})


class ContentsView(TemplateView):
    template_name = 'chapter/chapter_contents.html'

    def get(self, request, *args, **kwargs):
        try:
            if ChapterInfo.objects.get(pk=self.kwargs.get('chapter')).Use_Flag:
                pass
            else:
                messages.add_message(self.request, messages.WARNING, 'Chapter is not active.')
                raise ObjectDoesNotExist
        except:
            if '/students/' in request.path:
                return redirect('student_courseinfo_detail', pk=self.kwargs.get('course'))
            elif '/teachers/' in request.path:
                return redirect('teacher_courseinfo_detail', pk=self.kwargs.get('course'))
            else:
                return redirect('courseinfo_detail', pk=self.kwargs.get('course'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['chapterList'] = context['course'].chapterinfos.filter(Use_Flag=True)
        context['chapterList'] = sorted(context['chapterList'], key=lambda t: t.Chapter_No)
        context['chapter'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        courseID = context['chapter'].Course_Code.id
        chapterID = self.kwargs.get('chapter')
        context['chat_details'] = []
        context['connection_offline'] = False
        path = settings.MEDIA_ROOT

        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                context['data'] = json.load(json_file)
        except Exception as e:
            print(e)
            context['data'] = ""

        list_of_files = sorted(glob.iglob(path + '/chatlog/chapterchat' + str(chapterID) + '/*.txt'),
                               key=os.path.getctime, reverse=True)[:50]

        for latest_file in list_of_files:
            try:
                f = open(latest_file, 'r')
                if f.mode == 'r':
                    contents = f.read()
                    contents = contents.replace('`', '')
                    context['chat_details'].insert(0, contents)
                f.close()

            except Exception as e:
                pass
        return context


class NewContentsView(TemplateView):
    template_name = 'chapter/newContentViewer.html'  

    def get(self, request, *args, **kwargs):
        try:
            if ChapterInfo.objects.get(pk=self.kwargs.get('chapter')).Use_Flag:
                pass
            else:
                messages.add_message(self.request, messages.WARNING, 'Chapter is not active.')
                raise ObjectDoesNotExist
        except:
            if '/students/' in request.path:
                return redirect('student_courseinfo_detail', pk=self.kwargs.get('course'))
            elif '/teachers/' in request.path:
                return redirect('teacher_courseinfo_detail', pk=self.kwargs.get('course'))
            else:
                return redirect('courseinfo_detail', pk=self.kwargs.get('course'))
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['chapterList'] = context['course'].chapterinfos.filter(Use_Flag=True)
        context['chapterList'] = sorted(context['chapterList'], key=lambda t: t.Chapter_No)
        context['chapter'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        courseID = context['chapter'].Course_Code.id
        chapterID = self.kwargs.get('chapter')
        context['chat_details'] = []
        context['connection_offline'] = False
        path = settings.MEDIA_ROOT

        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                context['data'] = json.load(json_file)
        except Exception as e:
            print(e)
            context['data'] = ""

        list_of_files = sorted(glob.iglob(path + '/chatlog/chapterchat' + str(chapterID) + '/*.txt'),
                               key=os.path.getctime, reverse=True)[:50]

        for latest_file in list_of_files:
            try:
                f = open(latest_file, 'r')
                if f.mode == 'r':
                    contents = f.read()
                    contents = contents.replace('`', '')
                    context['chat_details'].insert(0, contents)
                f.close()

            except Exception as e:
                pass
        return context        


class OfflineContentsView(ContentsView):
    template_name = 'chapter/offlineviewer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['connection_offline'] = True
        return context


import shutil
import time


def get_static_files_info(request, *args, **kwargs):
    path = settings.MEDIA_ROOT
    now = datetime.now()
    list_of_files = [
        'static/lightbox',
        'static/3D_Viewer/model-viewer.js',
        'static/build/css/theme.min.css',
        'static/chapterPageBuilder/css/style-content.css',
        'static/chapterPageBuilder/js/owl-carousel/assets/owl.carousel.css',
        'static/chapterPageBuilder/js/owl-carousel/owl.carousel.js',
        'static/images/blankpage.jpg',
        'static/images/uLMS2019_Loading_SVG.svg',
        'static/js/modernizr.js',
        'static/vendorsx/bootstrap/dist/css/bootstrap.min.css',
        'static/vendorsx/font-awesome/css/font-awesome.min.css',

        'static/vendorsx/bootstrap/dist/css/bootstrap.css',
        'static/vendorsx/bootstrap/dist/css/bootstrap.min.css',
        'static/vendorsx/bootstrap/dist/js/bootstrap.min.js',
        'static/vendorsx/jquery/dist/jquery.min.js',
        'static/vendorsx/font-awesome',

        'static/pdfjs',
    ]
    if request.GET.get('force') == '1':
        json_data = {
            "last_modified": now.strftime("%m/%d/%Y, %H:%M:%S"),
            "list_of_files": list_of_files
        }
        with open(os.path.join(path, 'static_files_info.txt'), 'w') as json_file:
            json.dump(json_data, json_file)
        make_zip_file(list_of_files)
    else:
        if not os.path.exists(os.path.join(path, 'static_files_info.txt')):
            json_data = {
                "last_modified": now.strftime("%m/%d/%Y, %H:%M:%S"),
                "list_of_files": list_of_files
            }
            with open(os.path.join(path, 'static_files_info.txt'), 'w') as json_file:
                json.dump(json_data, json_file)
            make_zip_file(list_of_files)
        else:
            with open(os.path.join(path, 'static_files_info.txt')) as json_file:
                json_data = json.load(json_file)
            json_file_info_date = datetime.strptime(json_data['last_modified'], "%m/%d/%Y, %H:%M:%S")

            if os.path.exists(os.path.join(path, 'staticfiles.zip')):
                file_modified_time = time.ctime(os.path.getmtime(os.path.join(path, 'static_files_info.txt')))
                file_modified_time = datetime.strptime(file_modified_time, '%a %b %d %H:%M:%S %Y')
                if (file_modified_time > json_file_info_date):
                    json_data['last_modified'] = now.strftime("%m/%d/%Y, %H:%M:%S")
                    with open(os.path.join(path, 'static_files_info.txt'), 'w') as json_file:
                        json.dump(json_data, json_file)
                    make_zip_file(list_of_files)
            else:
                make_zip_file(list_of_files)

    last_modified = datetime.strptime(json_data['last_modified'], "%m/%d/%Y, %H:%M:%S").timestamp()
    return HttpResponse(int(last_modified))


def make_zip_file(list_of_files):
    path = settings.MEDIA_ROOT
    for src in list_of_files:
        dst = os.path.join(path, src)
        if not os.path.isdir(settings.BASE_DIR + '/WebApp/' + src):
            dstfolder = os.path.dirname(dst)
            if not os.path.exists(dstfolder):
                os.makedirs(dstfolder)
        if os.path.isdir(settings.BASE_DIR + '/WebApp/' + src):
            if (os.path.exists(dst)):  # if folder exists already, removes it and copy again
                shutil.rmtree(dst)
            shutil.copytree(settings.BASE_DIR + '/WebApp/' + src, dst)
        else:
            shutil.copy(settings.BASE_DIR + '/WebApp/' + src, dst)
            shutil.make_archive(path + '/staticfiles', 'zip', path + '/static')


def get_static_files(request):
    return redirect(settings.MEDIA_URL + '/staticfiles.zip')


from quiz.views import Sitting


def AchievementPage_Student(request, student_id):
    memberinfo = MemberInfo.objects.get(pk=student_id)
    sittings = Sitting.objects.filter(user=student_id)
    return render(request, 'WebApp/Student_Achievement.html', {'sittings': sittings, 'memberinfo': memberinfo})


def AchievementPage_All(request):
    CourseFilter = CourseInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True)
    Inningsfilter = InningInfo.objects.filter(Center_Code=request.user.Center_Code, End_Date__gte=datetime.now(),
                                              Use_Flag=True)

    # Linked relation between course and session
    # InningGroupFilter = InningGroup.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True)
    # Courses = dict()
    # for course in CourseFilter:
    #     temp = []
    #     for group in InningGroupFilter:
    #         if course.id==group.Course_Code.id:
    #             temp.append(group.id)
    #     Courses.update({course.id:temp})

    return render(request, 'WebApp/Achievement_all.html',
                  {"Inningsfilter": Inningsfilter, "CourseFilter": CourseFilter, "Courses": CourseFilter})


def AchievementPage_All_Ajax(request, Inningsfilter=None, studentfilter=None, CourseFilter=None):
    if Inningsfilter:
        # Inningsfilter = InningInfo.objects.filter(Center_Code=request.user.Center_Code,
        #                                       End_Date__gte=datetime.now()).values_list('Groups').order_by('id')
        CoursegroupFilter = InningInfo.objects.filter(id=Inningsfilter).values_list('Groups')
        # print('CoursegroupFilter', CoursegroupFilter)
        Student_GroupMappingFilter = GroupMapping.objects.filter(id__in=CoursegroupFilter,
                                                                 Center_Code=request.user.Center_Code).values_list(
            'Students').order_by('id')
        # print('Student_GroupMappingFilter', Student_GroupMappingFilter)
        studentfilter = MemberInfo.objects.filter(id__in=Student_GroupMappingFilter, Is_Student=True,
                                                  Center_Code=request.user.Center_Code)
        # print('studentfilter', studentfilter)
    elif CourseFilter:

        CoursegroupFilter = InningGroup.objects.filter(Course_Code=CourseFilter)
        # print('CoursegroupFilter', CoursegroupFilter)
        Inningsfilter = InningInfo.objects.filter(Center_Code=request.user.Center_Code,
                                                  Course_Group__in=CoursegroupFilter,
                                                  End_Date__gte=datetime.now()).values_list('Groups').order_by('id')
        # print('Inningsfilter', Inningsfilter)
        Student_GroupMappingFilter = GroupMapping.objects.filter(id__in=Inningsfilter,
                                                                 Center_Code=request.user.Center_Code).values_list(
            'Students').order_by('id')
        # print('Student_GroupMappingFilter', Student_GroupMappingFilter)
        studentfilter = MemberInfo.objects.filter(id__in=Student_GroupMappingFilter, Is_Student=True,
                                                  Center_Code=request.user.Center_Code)

        # print('studentfilter', studentfilter)

    return render(request, 'WebApp/AchievementPage_All_Ajax.html', {'studentfilter': studentfilter})


def gitpull(request):
    import subprocess
    process = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE)
    output = process.communicate()[0]
    return HttpResponse(output)


def ServiceWorker(request):
    with open('WebApp/templates/WebApp/PWA/pwabuilder-sw.js', 'r') as f:
        data = f.read()
    return HttpResponse(data, content_type='text/javascript')


def OfflineApp(request):
    with open('WebApp/templates/WebApp/PWA/offline.html', 'r') as f:
        data = f.read()
    return HttpResponse(data, )


def manifestwebmanifest(request):
    with open('WebApp/templates/WebApp/PWA/manifest.webmanifest', 'r') as f:
        data = f.read()
    return HttpResponse(data, )


class SessionManagerUpdateView(UpdateView):
    model = InningManager
    form_class = InningManagerForm
    template_name = 'WebApp/sessionmanager_form.html'

    def get_object(self):
        session_Manager = None
        if InningManager.objects.filter(sessioninfoobj__pk=self.kwargs.get('pk')).exists():
            session_Manager = InningManager.objects.get(sessioninfoobj__pk=self.kwargs.get('pk'))
        else:
            session_Manager = InningManager.objects.create(
                sessioninfoobj=InningInfo.objects.get(pk=self.kwargs.get('pk')))
        return session_Manager

    def form_valid(self, form):
        if form.is_valid():
            form.save()
            messages.add_message(self.request, messages.SUCCESS, 'Session Managers Updated.')
            # return super().form_valid(form)
            return redirect('inninginfo_detail', self.kwargs.get('pk'))

    def get_form_kwargs(self):
        kwargs = super(SessionManagerUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


def viewteacherAttendance(request, attend_date, courseid, teacherid):
    attend_date = datetime.strptime(str(attend_date), "%m%d%Y").strftime("%m%d%Y")
    print(attend_date)
    path = os.path.join(settings.MEDIA_ROOT, ".teacherAttendanceData", str(courseid), attend_date)

    teacher_data_file = os.path.join(path, str(teacherid) + '.txt')

    if os.path.isfile(teacher_data_file):
        with open(teacher_data_file) as json_file:
            data = json.load(json_file)
            start_time = data['start_time']
            end_time = data['end_time']
            numberoftimesopened = int(data['numberoftimesopened'])
            chapters = data['chapters']
            print(data)
            return JsonResponse(data)
    else:
        return HttpResponse("No attendance recorded", status=500)


from django.contrib.auth import authenticate, login as auth_login


def loginforappredirect(request, username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        auth_login(request, user)
        if request.user.is_authenticated:
            if 'url' in request.GET:
                url = request.GET.get('url')
                return redirect(
                    url
                )
            else:
                return HttpResponse('Login Success', status=200)
        else:
            return HttpResponse('User is not authenticated', status=500)
    else:
        return HttpResponse('Incorrect Username or Password', status=500)


def CourseProgressView(request, coursepk, inningpk=None):
    session_list = []
    courseObj = get_object_or_404(CourseInfo, pk=coursepk)
    chapters_list = courseObj.chapterinfos.all().order_by('Chapter_No')
    list_of_students = []
    # student_data = []
    if '/teachers' in request.path:
        basefile = "teacher_module/base.html"
    elif '/teachers' or '/students' not in request.path:
        basefile = "base.html"
    if coursepk:
        if '/teachers' in request.path:
            inning_info = InningInfo.objects.filter(Course_Group__Teacher_Code__pk=request.user.pk,
                                                    Course_Group__Course_Code__pk=coursepk, Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct()
        else:
            inning_info = InningInfo.objects.filter(Course_Group__Course_Code__pk=coursepk, Use_Flag=True,
                                                    End_Date__gt=datetime.now()).distinct()
        session_list.append(inning_info)

        if inning_info.count() > 0:
            if inningpk:
                innings = get_object_or_404(inning_info, pk=inningpk)
            else:
                innings = inning_info.all().first()

            if MemberInfo.objects.filter(pk__in=innings.Groups.Students.all()).exists():
                list_of_students = MemberInfo.objects.filter(pk__in=innings.Groups.Students.all())
            student_data = getCourseProgress(courseObj, list_of_students, chapters_list)
        else:
            messages.add_message(request, messages.ERROR,
                                 'The course is not assosiated with any innings. Please contact administrator')
            context = {
                'course': courseObj,
                'chapter_list': chapters_list,
                'basefile': basefile,
            }
            return render(request, 'teacher_module/chapterProgress.html', context=context)

    context = {
        'session_list': session_list,
        'student_progress_data': student_data,
        'number_of_students': list_of_students.count(),
        'course': courseObj,
        'inning': innings,
        'chapter_list': chapters_list,
        'basefile': basefile,
    }
    return render(request, 'teacher_module/chapterProgress.html', context=context)


def chapterProgressRecord(courseid, chapterid, studentid, fromcontents=False, currentPageNumber=None, totalPage=None,
                          studytimeinseconds=None, createFile=True, isjson=False
                          ):
    jsondata = None
    path = os.path.join(settings.MEDIA_ROOT, ".chapterProgressData", courseid, chapterid)
    try:
        os.makedirs(path)  # Creates the directories and subdirectories structure
    except Exception as e:
        pass
    student_data_file = os.path.join(path, studentid + '.txt')
    try:
        with open(student_data_file) as outfile:
            jsondata = json.load(outfile)
        isjson = True
    except FileNotFoundError:
        print(FileNotFoundError)
    except JSONDecodeError:
        print(JSONDecodeError)
        # with open(student_data_file) as outfile:
        #     if outfile.read()[0] == '{' and 'contents' in outfile.read():
        #         return
        #     else:
        #         isjson = False
    if os.path.isfile(student_data_file):
        if fromcontents:
            if currentPageNumber is None:
                return jsondata

            jsondata['contents']['totalstudytime'] = int(jsondata['contents']['totalstudytime']) + int(
                studytimeinseconds)
            jsondata['contents']['laststudydate'] = datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S")

            if int(currentPageNumber) > int(jsondata['contents']['currentpagenumber']):
                jsondata['contents']['currentpagenumber'] = currentPageNumber
                jsondata['contents']['totalPage'] = totalPage
            with open(student_data_file, "w") as outfile:
                json.dump(jsondata, outfile, indent=4)
    else:
        if createFile:
            if fromcontents:
                jsondata = {
                    "contents": {
                        "laststudydate": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
                        "totalstudytime": studytimeinseconds,
                        "currentpagenumber": currentPageNumber,
                        "totalPage": totalPage,
                    },
                }
            else:
                return None
            # student_file = open(student_data_file, "w+")
            with open(student_data_file, "w+") as outfile:
                json.dump(jsondata, outfile, indent=4)
        else:
            return None
    return jsondata


def getCourseProgress(courseObj, list_of_students, chapters_list, student_data=None):
    student_data = []
    for chapter in chapters_list:
        for x in list_of_students:
            jsondata = chapterProgressRecord(str(courseObj.pk), str(chapter.pk), str(x.id),
                                             createFile=False)
            if jsondata is not None:
                if jsondata['contents']['totalPage'] and jsondata['contents']['currentpagenumber']:
                    if int(jsondata['contents']['totalPage']) > 0 and int(
                            jsondata['contents']['currentpagenumber']) > 0:
                        progresspercent = int(jsondata['contents']['currentpagenumber']) * 100 / int(
                            jsondata['contents']['totalPage'])
                else:
                    progresspercent = 0
            else:
                progresspercent = 0

            student_quiz = Quiz.objects.filter(chapter_code=chapter)
            # If the quiz is taken by the student multiple times, then just get the latest attempted quiz.

            student_result = Sitting.objects.order_by('-end').filter(user=x, quiz__in=student_quiz)._clone()
            # student_result = Sitting.objects.order_by('-end').filter(user=x, quiz__in=student_quiz)
            total_quiz_percent_score = 0
            temp = []
            for z in student_result:
                if z.quiz.pk in temp:
                    # student_result.get(pk=z.pk).delete()
                    student_result = student_result.exclude(pk=z.pk)
                else:
                    temp.append(z.quiz.pk)
                    total_quiz_percent_score += float(z.get_percent_correct)

            # Attendance here means chapter completion.
            ''' Attendance is present if the student has spent time as mentioned in the chapter model mustreadtime
                field and the chapter progress is 100% '''
            if chapter.mustreadtime and jsondata:
                if jsondata['contents']['totalstudytime']:
                    attendance = int(jsondata['contents'][
                                         'totalstudytime']) >= chapter.mustreadtime and progresspercent >= 100 if jsondata else False
                else:
                    attendance = False
            else:
                attendance = None
            if jsondata:
                student_data.append(
                    {
                        'student': x,
                        'chapter': {
                            'chapterObj': chapter,
                            'laststudydate': datetime.strptime(jsondata['contents'][
                                                                   'laststudydate'], "%m/%d/%Y %H:%M:%S").strftime(
                                "%Y/%m/%d %H:%M:%S") if jsondata['contents']['laststudydate'] is not None else None,
                            'totalstudytime': timedelta(seconds=int(jsondata['contents']['totalstudytime'])) if
                            jsondata['contents']['totalstudytime'] is not None else "00:00:00",
                            'currentpagenumber': int(
                                jsondata['contents']['currentpagenumber']) if jsondata['contents'][
                                                                                  'currentpagenumber'] is not None else None,
                            'totalPage': int(
                                jsondata['contents']['totalPage']) if jsondata['contents'][
                                                                          'totalPage'] is not None else None,
                            'progresspercent': progresspercent,
                            'attendance': attendance,
                        },
                        'quiz': {
                            'quiz_count': student_quiz.count(),
                            'completed_quiz': student_result.filter(complete=True).count(),
                            'progress': student_result.filter(
                                complete=True).count() * 100 / student_quiz.count() if student_quiz.count() is not 0 else 0,
                            # 'completed_quiz_score': student_result.filter(complete=True).values().aggregate(Sum('current_score')),
                            # 'completed_quiz_totalscore': student_quiz.aggregate(Sum('get_max_score'))
                            'avg_percent_score': float(total_quiz_percent_score / student_result.filter(
                                complete=True).count()) if student_result.filter(complete=True).count() > 0 else 0
                        }
                    },
                )
            else:
                student_data.append(
                    {
                        'student': x,
                        'chapter': {
                            'chapterObj': chapter,
                            'laststudydate': None,
                            'totalstudytime': "00:00:00",
                            'currentpagenumber': None,
                            'totalPage': None,
                            'progresspercent': progresspercent,
                            'attendance': attendance,
                        },
                        'quiz': {
                            'quiz_count': student_quiz.count(),
                            'completed_quiz': student_result.filter(complete=True).count(),
                            'progress': student_result.filter(
                                complete=True).count() * 100 / student_quiz.count() if student_quiz.count() is not 0 else 0,
                            # 'completed_quiz_score': student_result.filter(complete=True).values().aggregate(Sum('current_score')),
                            # 'completed_quiz_totalscore': student_quiz.aggregate(Sum('get_max_score'))
                            'avg_percent_score': float(total_quiz_percent_score / student_result.filter(
                                complete=True).count()) if student_result.filter(complete=True).count() > 0 else 0
                        }
                    },
                )
    return student_data


def studentChapterLog(chapterid, studentid, type, createFile=True, isjson=False):
    date = datetime.now().strftime('%Y%m%d')
    path = os.path.join(settings.MEDIA_ROOT, ".studentChapterLog", date)
    try:
        os.makedirs(path)  # Creates the directories and subdirectories structure
    except Exception as e:
        pass
    student_data_file = os.path.join(path, studentid + '.txt')
    try:
        with open(student_data_file) as outfile:
            jsondata = json.load(outfile)
        isjson = True
    except:
        isjson = False
    if os.path.isfile(student_data_file) and isjson:
        if not type:
            return jsondata
        newdata = {
            "chapterid": chapterid,
            "visittime": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
            "type": type,  # type refers to when the function was called. i.e. upon entering viewer or closing
        }
        jsondata.append(newdata)
        with open(student_data_file, "w+") as outfile:
            json.dump(jsondata, outfile, indent=4)
    else:
        if createFile:
            jsondata = [
                {
                    "chapterid": chapterid,
                    "visittime": datetime.utcnow().strftime("%m/%d/%Y %H:%M:%S"),
                    "type": type,  # type refers to when the function was called. i.e. upon entering viewer or closing
                },
            ]

            with open(student_data_file, "w+") as outfile:
                json.dump(jsondata, outfile, indent=4)
        else:
            return None
    return jsondata


def getListOfFiles(dirName, studentid):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            # conv and compare is added to get only the files of 7days
            conv = datetime.strptime(entry, '%Y%m%d').date()
            compare = (datetime.today() - timedelta(days=30)).date()
            if (compare < conv):
                allFiles = allFiles + getListOfFiles(fullPath, studentid)
        elif entry == str(studentid) + '.txt':
            allFiles.append(fullPath)

    return allFiles


def StudentChapterProgressView(request, courseid, chapterid, studentid):
    context = dict()
    courseObj = get_object_or_404(CourseInfo, pk=courseid)
    chapterObj = get_object_or_404(ChapterInfo, pk=chapterid)
    studentObj = get_object_or_404(MemberInfo, pk=studentid)

    if '/teachers' in request.path:
        basefile = "teacher_module/base.html"
    elif '/teachers' or '/students' not in request.path:
        basefile = "base.html"
    context['basefile'] = basefile

    path = os.path.join(settings.MEDIA_ROOT, ".studentChapterLog")
    date_dir = getListOfFiles(path, studentid)
    temp = []
    for filepath in date_dir:
        flag = 0
        dirname = os.path.split(os.path.split(filepath)[0])[1]
        date = datetime.strptime(dirname, '%Y%m%d').date()
        try:
            with open(filepath) as outfile:
                jsondata = json.load(outfile)
        except:
            jsondata = ''
        if jsondata:
            temp_json_data = []
            for data in jsondata:
                if data['chapterid'] == str(chapterid):
                    converted_datetime = datetime.strptime(data['visittime'], '%m/%d/%Y %H:%M:%S')
                    data['visittime'] = converted_datetime
                    temp_json_data.append(data)
                    flag = 1
            if flag == 1:
                temp.append({'date': date, 'data': temp_json_data})
    context['object'] = temp
    context['course'] = courseObj
    context['chapter'] = chapterObj
    context['student'] = studentObj
    return render(request, 'teacher_module/progressdetail.html', context=context)


def loaderverifylink(request):
    return render(request, 'loaderio.html')


def notice_view_create(request):
    if request.method == 'POST':
        print(request.POST['user_code'], request.POST['notice_code'], request.POST['dont_show'])
        user_code = request.user
        notice_code = Notice.objects.get(id=request.POST['notice_code'])
        if NoticeView.objects.filter(user_code=user_code, notice_code=notice_code).exists():
            obj = NoticeView.objects.get(user_code=user_code, notice_code=notice_code)
        else:
            obj = NoticeView()
            obj.user_code = user_code
            obj.notice_code = notice_code
        if request.POST['dont_show'] == 'true':
            obj.dont_show = True
        else:
            obj.dont_show = False
        obj.save()
        return JsonResponse({'status': 'Success', 'msg': 'Added status'})
