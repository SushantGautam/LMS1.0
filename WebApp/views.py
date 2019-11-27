import json
import os
import shutil
import uuid
import zipfile  # For import/export of compressed zip folder
from datetime import datetime

import pandas as pd
# import vimeo  # from PyVimeo for uploading videos to vimeo.com
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
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.db.models import Q

from LMS.settings import BASE_DIR
from forum.models import Thread, Topic
from forum.views import get_top_thread_keywords, NodeGroup
from quiz.models import Question, Quiz
from survey.models import SurveyInfo
from .forms import CenterInfoForm, CourseInfoForm, ChapterInfoForm, SessionInfoForm, InningInfoForm, UserRegisterForm, \
    AssignmentInfoForm, QuestionInfoForm, AssignAssignmentInfoForm, MessageInfoForm, \
    AssignAnswerInfoForm, InningGroupForm, GroupMappingForm, MemberInfoForm, ChangeOthersPasswordForm, MemberUpdateForm
from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
    CourseInfo, ChapterInfo, AssignmentInfo, AssignmentQuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, Events


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
    return render(request,'error_page/page_400.html',data)

def error_403(request, exception):
    data = {}
    return render(request,'error_page/page_403.html',data)

def error_404(request, exception):
    data = {}
    return render(request,'error_page/page_404.html',data)

def error_500(request):
    data = {}
    return render(request,'error_page/page_500.html',data)


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
            thread = Thread.objects.visible().filter(user__Center_Code=request.user.Center_Code).order_by('-pub_date')[:5]
            wordCloud = Thread.objects.filter(user__Center_Code=request.user.Center_Code)
            thread_keywords = get_top_thread_keywords(request, 10)
            course = CourseInfo.objects.filter(Use_Flag=True, Center_Code=request.user.Center_Code).order_by('-Register_DateTime')[:5]
            coursecount = CourseInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True).count
            studentcount = MemberInfo.objects.filter(Is_Student=True, Center_Code=request.user.Center_Code).count
            teachercount = MemberInfo.objects.filter(Is_Teacher=True, Center_Code=request.user.Center_Code).count
            threadcount = Thread.objects.visible().filter(user__Center_Code=request.user.Center_Code).count
            totalcount = MemberInfo.objects.filter(Center_Code=request.user.Center_Code).count
            surveycount = SurveyInfo.objects.filter(Q(Use_Flag=True), Q(Center_Code=request.user.Center_Code) | Q(Center_Code=None), Q(End_Date__gte=datetime.now()))[:5]
            sessioncount = InningInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True,
                                                     End_Date__gte=datetime.now())[:5]

            # return HttpResponse("default home")
            return render(request, "WebApp/homepage.html",
                          {'course': course, 'coursecount': coursecount, 'studentcount': studentcount,
                           'teachercount': teachercount,
                           'threadcount': threadcount, 'totalcount': totalcount, 'thread': thread,
                           'wordCloud': wordCloud, 'get_top_thread_keywords': thread_keywords,
                           'surveycount': surveycount,
                           'sessioncount': sessioncount})
        elif request.user.Is_Student:
            return redirect('student_home')
        elif request.user.Is_Teacher:
            return redirect('teacher_home')
        elif request.user.Is_Parent:
            return redirect('parent_home')
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


class MemberInfoListView(ListView):
    model = MemberInfo

    def get_queryset(self):
        return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code, Use_Flag=True)


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


def ImportCsvFile(request):
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

        df = pd.read_csv(path)
        # Drop empty row of excel csv file
        df = df.dropna(how='all')
        saved_id = []
        for i in range(len(df)):
            try:
                obj = MemberInfo()
                obj.username = df.iloc[i]['Username']
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

                if df.iloc[i]['Teacher'] == 1:
                    obj.Is_Teacher = True
                else:
                    obj.Is_Teacher = False

                if df.iloc[i]['Student'] == 1:
                    obj.Is_Student = True
                else:
                    obj.Is_Student = False

                obj.Center_Code = CenterInfo.objects.get(id=request.user.Center_Code.id)
                obj.set_password('00000')
                obj.save()
                saved_id.append(obj.id)

            except:
                for j in saved_id:
                    MemberInfo.objects.filter(id=j).delete()
                msg = "Can't Upload all data. Problem in " + str(i + 1) + "th row of data while uploading."
                return JsonResponse(data={"message": msg, "class": "text-danger", "rmclass": "text-success"})
        return JsonResponse(data={"message": "All data has been Uploaded Sucessfully", "class": "text-success",
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


class MemberInfoDetailView(DetailView):
    model = MemberInfo


class MemberInfoUpdateView(UpdateView):
    model = MemberInfo
    form_class = MemberUpdateForm


class MemberInfoDeleteView(DeleteView):
    model = MemberInfo
    success_url = reverse_lazy('memberinfo_list')

    def post(self, request, *args, **kwargs):
        redirect_link = self.request.POST.get('redirect','memberinfo_list')
        try:
            self.delete(request, *args, **kwargs)
            messages.success(request,"The user is deleted Successfully")
            return redirect(redirect_link)
        except:
            messages.error(request,
                           "You can't delete this user instead you can turn off the status value which will disable the user.")
            return redirect(redirect_link)


class CourseInfoListView(ListView):
    model = CourseInfo
    paginate_by = 8

    def get_queryset(self):
        qs = self.model.objects.filter(Center_Code=self.request.user.Center_Code)
        query = self.request.GET.get('query')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__contains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs


class CourseInfoCreateView(CreateView):
    model = CourseInfo
    form_class = CourseInfoForm


class CourseInfoDetailView(DetailView):
    model = CourseInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Quiz.objects.filter(course_code=self.kwargs.get('pk'))
        context['topic'] = Topic.objects.filter(course_associated_with=self.kwargs.get('pk'))
        context['exam_quiz'] = Quiz.objects.filter(exam_paper=True, course_code=self.object)
        return context


class CourseInfoUpdateView(UpdateView):
    model = CourseInfo
    form_class = CourseInfoForm


def CourseInfoDeleteView(request, pk):
    if request.method == 'POST':
        try:
            # return self.delete(request, *args, **kwargs)
            Obj = CourseInfo.objects.get(pk=pk)
            Obj.delete()
            return redirect('courseinfo_list')

        except:
            messages.error(request,
                           "Cannot delete courses with chapters")
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

    def post(self, request, *args, **kwargs):
        Obj = ChapterInfo()
        Obj.Chapter_No = request.POST["Chapter_No"]
        Obj.Chapter_Name = request.POST["Chapter_Name"]
        Obj.Summary = request.POST["Summary"]
        if request.POST["Use_Flag"] == 'false':
            Obj.Use_Flag = False
        else:
            Obj.Use_Flag = True
        Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


class ChapterInfoDetailView(DetailView):
    model = ChapterInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(ChapterInfo, Course_Code=self.kwargs.get('course'), pk = self.kwargs.get('pk'))
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        context['post_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), post_test=True)
        context['pre_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), pre_test=True)
        context['datetime'] = datetime.now()
        return context


class ChapterInfoDeleteView(DeleteView):
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


class ChapterInfoUpdateView(UpdateView):
    model = ChapterInfo
    form_class = ChapterInfoForm

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.now()
        return context

class InningInfoDetailView(DetailView):
    model = InningInfo


class InningInfoUpdateView(UpdateView):
    model = InningInfo
    form_class = InningInfoForm

    def get_form_kwargs(self):
        kwargs = super(InningInfoUpdateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datetime'] = datetime.now()
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


class InningGroupDetailView(DetailView):
    model = InningGroup


class InningGroupUpdateView(UpdateView):
    model = InningGroup
    form_class = InningGroupForm

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


class GroupMappingCreateView(CreateView):
    model = GroupMapping
    form_class = GroupMappingForm

    def get_form_kwargs(self):
        kwargs = super(GroupMappingCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs


class GroupMappingDetailView(DetailView):
    model = GroupMapping


class GroupMappingUpdateView(UpdateView):
    model = GroupMapping
    form_class = GroupMappingForm

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
        Obj.Assignment_Deadline = request.POST["Assignment_Deadline"]
        Obj.Use_Flag = request.POST["Use_Flag"].capitalize()
        Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
        Obj.Chapter_Code = ChapterInfo.objects.get(id=request.POST["Chapter_Code"])
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
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
            Obj.Assignment_Deadline = request.POST["Assignment_Deadline"]
            Obj.Use_Flag = request.POST["Use_Flag"].capitalize()
            Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
            Obj.Chapter_Code = ChapterInfo.objects.get(id=request.POST["Chapter_Code"])
            Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
            Obj.save()

            return JsonResponse(
                data={'Message': 'Success'}
            )

        except:
            return JsonResponse(
                data={'Message': 'Fail'}
            )


class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['datetime'] = datetime.now()
        return context


class AssignmentInfoUpdateView(UpdateView):
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
        'data': data
    }
    return render(request, 'WebApp/chapterbuilder.html', context)

def save_file(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        media_type = request.POST['type']
        # old_file = request.POST['old']
        path = ''
        if request.FILES['file-0']:
            media = request.FILES['file-0']
            if media_type == 'pic':
                if (media.size / 1024) > 2048:
                    return JsonResponse(data={"message": "File size exceeds 2MB"}, status=500)
            path = settings.MEDIA_ROOT

            name = (str(uuid.uuid4())).replace('-', '') + '.' + media.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            filename = fs.save(name, media)
            # if old_file is not '0':
            #     deletefile(request)
        return JsonResponse(data={"message": "success", "media_name": name})

def deletechapterfile(request):
    if request.method == 'POST' and request.user.is_authenticated:
        old_file = json.loads(request.POST['old'])
        print(old_file)
        for value in old_file.values():
            for x in value:
                if os.path.exists(os.path.join(BASE_DIR, x[1:])):
                    os.remove(os.path.join(BASE_DIR, x[1:]))
                    return JsonResponse({'message':'deletion success'})
    return HttpResponse('')

def save_3d_file(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        path = ''
        if request.FILES['objfile']:
            obj = request.FILES['objfile']
            try:
                mtl = request.FILES['mtlfile']
            except:
                mtl = None
            path = settings.MEDIA_ROOT

            name = (str(uuid.uuid4())).replace('-', '') #same name for .obj and .mtl file
            objname = name + '.' + obj.name.split('.')[-1]
            fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            filename = fs.save(objname, obj)
            if mtl is not None:
                mtlname = name + '.' + mtl.name.split('.')[-1]
                fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
                filename = fs.save(mtlname, mtl)
        return JsonResponse(data={"message": "success", "objname": objname})        

@csrf_exempt
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
        name = (str(uuid.uuid4()).replace('-', '')) + '.' + media.name.split('.')[-1]
        fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
        filename = fs.save(name, media)
        return JsonResponse({'media_name': name})
    '''
        # #video uploading to vimeo.com

        # standard Account
        # v = vimeo.VimeoClient(
        #     token='7a954bb83b66a50a95efc2d1cfdd484a',
        #     key='22a07cf36ea4aa33c9e61a38deacda1476b81809',
        #     secret='1mX35wDF+GwizSs2NN/ns42c4qj5SFzguquEm2lQcbsmUYrcztOO099Dz3GjlPQvQELcbKPwtb9HWiMikZlgDvL/OcevzTiE13d9Cc4B8CH25BY01FN5LvUcT2KZfg4'
        # )
        # Premium Account
        v = vimeo.VimeoClient(
            token='3b42ecf73e2a1d0088dd677089d23e32',
            key='3b55a8ee9a7d0702c787c18907e79ceaa535b0e3',
            secret='KU1y3Bl/ZWj3ZgEzi7g5dtr8bESaBkqBtH5np1QUKBI0zLDvxteNURzRW09kl6QXqKLnCjtV15r0VwV+9nsYu6GmNFw5vjb4zKDWqpsWT+qPBn2I23n+ckLglgIvHmBh'
        )

        # media = '{path to a video on the file system}'

        uri = v.upload(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + name, data={
            'name': name,
        })

        response = v.get(uri).json()
        status = response['status']
        videoid = response['uri'].split('/')[-1]

        url = 'https://api.vimeo.com/me/projects/772975/videos/' + videoid  # Premium account Folder
        # url = 'https://api.vimeo.com/me/projects/936814/videos/'+videoid    #Standard Account Folder
        v.put(url)
        print(response['status'])

        while status == 'transcode_starting' or status == 'transcoding':
            r = v.get(uri + '?fields=status').json()
            status = r['status']
        return JsonResponse({'link': response['link'], 'media_name': name, 'html': response['embed']['html']})
    '''


@csrf_exempt
def save_json(request):
    if request.method == "POST":
        jsondata = json.loads(request.POST['json'])
        htmldata = json.loads(request.POST['htmlfile'])
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        path = settings.MEDIA_ROOT

        # creates directory structure if not exists
        make_directory_if_not_exists(courseID, chapterID)

        # for saving json data for viewing purposes
        with open(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + chapterID + '.txt', 'w') as outfile:
            json.dump(jsondata, outfile, indent=4)

        # for saving all html data of page for API purposes
        with open(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + chapterID + 'html.txt',
                  'w') as outfile:
            json.dump(htmldata, outfile, indent=4)

        chapterObj = ChapterInfo.objects.get(id=chapterID)
        chapterObj.Page_Num = int(jsondata['numberofpages'])
        chapterObj.save()

        return JsonResponse(data={"message": "Json Saved"})


def export_chapter(request, course, chapter):
    coursename = CourseInfo.objects.get(id=course).Course_Name
    path = settings.MEDIA_ROOT
    dir_name = path + '/chapterBuilder/' + str(course) + '/' + str(chapter)
    if not os.path.exists(dir_name):
        return HttpResponse('No directory')
    zipfile = shutil.make_archive(path + '/export/' + str(coursename) + '_Chapter' + str(chapter), 'zip', dir_name)

    return redirect(settings.MEDIA_URL + '/export/' + str(coursename) + '_Chapter' + str(chapter) + '.zip')


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
                my_json = json_file.read().decode('utf8').replace("'", '"')

                data = json.loads(my_json)

                if not all(k in data for k in ("numberofpages", "pages")):
                    return JsonResponse({'status': 'false', 'message': "Not valid zip"}, status=500)
                elif data['numberofpages'] is 0:
                    return JsonResponse({'status': 'false', 'message': "Not valid zip"}, status=500)

                # check if numberofpages and pages are in the dictionary or not

            continue
        zip.extract(file, storage_path)  # extract the file to current folder if it is a text file
    return JsonResponse(data)
    # -------------------------------------------------------------------------------------------------------

@xframe_options_exempt
def ThreeDViewer(request, urlpath=None):
    print(urlpath, "urlpath")
    mtlurlpath = None

    if not urlpath:
        urlpath = "static/3D_Viewer/Sample.obj"
        mtlurlpath = "static/3D_Viewer/Sample.mtl"
    else:
        mtlpath_expected = BASE_DIR +"/" + urlpath[:-4]+".mtl"
        print("got it mtlpath_expected", mtlpath_expected)
        if os.path.isfile(mtlpath_expected):
            print("file exist ", mtlpath_expected," url is:", mtlurlpath)
            mtlurlpath = (urlpath[:-4] if urlpath else '') + ".mtl"
        else:
            print("MTL doesnt exist", mtlpath_expected)
            mtlurlpath = "static/3D_Viewer/none.mtl"

    return render(request, '3D_Viewer/render_template.html', {'objpath': urlpath, 'mtlpath': mtlurlpath})

class ContentsView(TemplateView):
    template_name = 'chapter/chapter_contents.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['chapter'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        courseID = context['chapter'].Course_Code.id
        chapterID = self.kwargs.get('chapter')
        path = settings.MEDIA_ROOT
        
        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                context['data'] = json.load(json_file)
        except Exception as e:
            print(e)
            context['data'] = ""
        return context

from quiz.views import QuizUserProgressView, Sitting, Progress
def AchievementPage_Student(request, student_id):
    sittings =  Sitting.objects.filter(user=request.user)
    return render(request, 'WebApp/Student_Achievement.html', {'sittings':sittings})



from WebApp.forms import AchievementPage_All_form
def AchievementPage_All(request):
    CourseFilter = CourseInfo.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True)
    Inningsfilter = InningInfo.objects.filter(Center_Code=request.user.Center_Code, End_Date__gte=datetime.now(), Use_Flag=True)

    # Linked relation between course and session
    # InningGroupFilter = InningGroup.objects.filter(Center_Code=request.user.Center_Code, Use_Flag=True)
    # Courses = dict()
    # for course in CourseFilter:
    #     temp = []
    #     for group in InningGroupFilter:
    #         if course.id==group.Course_Code.id:
    #             temp.append(group.id)
    #     Courses.update({course.id:temp})
    
    return render(request, 'WebApp/Achievement_all.html', {"Inningsfilter":Inningsfilter,  "CourseFilter":CourseFilter, "Courses": CourseFilter})

def AchievementPage_All_Ajax(request, Inningsfilter=None, studentfilter=None, GroupMappingFilter=None):
    Inningsfilter = InningInfo.objects.filter(Center_Code=request.user.Center_Code, End_Date__gte=datetime.now()).values_list('Groups').order_by('id')
    Student_GroupMappingFilter = GroupMapping.objects.filter(id__in= Inningsfilter, Center_Code=request.user.Center_Code).values_list('Students').order_by('id')
    studentfilter = MemberInfo.objects.filter(id__in=Student_GroupMappingFilter, Is_Student=True, Center_Code=request.user.Center_Code)

    return render(request, 'WebApp/AchievementPage_All_Ajax.html', {'studentfilter':studentfilter})

