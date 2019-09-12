from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.views import LogoutView, LoginView, PasswordContextMixin
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import DetailView, ListView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import FormView
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from PIL import Image
import os
import json

from forum.models import Thread
from forum.views import get_top_thread_keywords
from survey.models import SurveyInfo
from quiz.models import Question

from .forms import CenterInfoForm, CourseInfoForm, ChapterInfoForm, SessionInfoForm, InningInfoForm, UserRegisterForm,\
                   AssignmentInfoForm, QuestionInfoForm, AssignAssignmentInfoForm, MessageInfoForm, \
                   AssignAnswerInfoForm, InningGroupForm, GroupMappingForm, MemberInfoForm, ChangeOthersPasswordForm

from .models import CenterInfo, MemberInfo, SessionInfo, InningInfo, InningGroup, GroupMapping, MessageInfo, \
                    CourseInfo, ChapterInfo, AssignmentInfo, QuestionInfo, AssignAssignmentInfo, AssignAnswerInfo, Events
from datetime import datetime
from forum.models import Thread, Topic, Post, ForumAvatar, NodeGroup
from forum.views import get_top_thread_keywords, NodeGroup, TopicView, ThreadView

import json


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
    try:
        center = CenterInfo.objects.get(Center_Name=request.user.Center_Code)
    except:
        center = None
        pass
    return render(request, 'WebApp/profile.html', {"center": center})


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

        if request.user.Is_CenterAdmin:
            thread = Thread.objects.order_by('-pub_date')[:5]
            wordCloud = Thread.objects.all()
            thread_keywords = get_top_thread_keywords(request, 10)
            course = CourseInfo.objects.order_by('-Register_DateTime')[:4]
            coursecount = CourseInfo.objects.count()
            studentcount = MemberInfo.objects.filter(Is_Student=True, Center_Code=request.user.Center_Code).count
            teachercount = MemberInfo.objects.filter(Is_Teacher=True, Center_Code=request.user.Center_Code).count
            threadcount = Thread.objects.count()
            totalcount = MemberInfo.objects.filter(Center_Code=request.user.Center_Code).count

            # return HttpResponse("default home")
            return render(request, "WebApp/homepage.html",
                          {'course': course, 'coursecount': coursecount, 'studentcount': studentcount,
                           'teachercount': teachercount,
                           'threadcount': threadcount, 'totalcount': totalcount, 'thread': thread,
                           'wordCloud': wordCloud, 'get_top_thread_keywords': thread_keywords})
        if request.user.Is_Student:
            return redirect('student_home')
        if request.user.Is_Teacher:
            return redirect('teacher_home')
        if request.user.Is_Parent:
            return redirect('parent_home')
        else:
            msg = "Sorry you aren't assigned to any member type. User must be assigned to a member type\
                to go to their respective dashboard. Please request your center admin or super admin to assign you as one type of member"
            return render(request, "WebApp/splash_page.html", {'msg': msg})

    else:
        return render(request, "WebApp/splash_page.html")


def editprofile(request):
    if not request.user.is_authenticated:
        return HttpResponse("you are not authenticated", {'error_message': 'Error Message Customize here'})

    post = get_object_or_404(MemberInfo, pk=request.user.id)
    if request.method == "POST":

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

        # if request.user.isAdmin:
        #     form = UserUpdateFormForAdmin(request.POST, request.FILES, instance=post)

        if form.is_valid():
            # post.date_last_update = datetime.now()
            post.save()
            return redirect('start')
    else:

        # form = UserUpdateForm(instance=post)
        form = UserUpdateForm(request.POST, request.FILES, instance=post)

        # if request.user.isAdmin == 1:
        #     form = UserUpdateFormForAdmin(instance=post)

    return render(request, 'registration/editprofile.html', {'form': form})


class register(CreateView):
    model = MemberInfo
    form_class = UserRegisterForm
    success_url = reverse_lazy('loginsuccess')
    template_name = 'registration/register.html'

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
            messages.success(request, 'Your password was successfully updated!')

            return redirect('user_profile')
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
        return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code,Use_Flag=True)


class MemberInfoListViewInactive(ListView):
    model = MemberInfo
    template_name = 'WebApp/memberinfo_list_inactive.html'

    def get_queryset(self):
        return MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code,Use_Flag=False)



class MemberInfoCreateView(CreateView):
    model = MemberInfo
    form_class = MemberInfoForm


def MemberInfoActivate(request,pk):
    try:
        obj = MemberInfo.objects.get(pk=pk)
        obj.Use_Flag=True
        obj.save()
    except:
        messages.error(request,'Cannot perform the action. Please try again later')
    
    return redirect('memberinfo_list_inactive')



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
    form_class = MemberInfoForm


class MemberInfoDeleteView(DeleteView):
    model = MemberInfo
    success_url = reverse_lazy('memberinfo_list')

    def post(self, request, *args, **kwargs):
        try:
            return self.delete(request, *args, **kwargs)
        except:
            messages.error(request,
                           "You can't delete this user instead you can turn off the status value which will disable the user.")
            return redirect('memberinfo_list')


class CourseInfoListView(ListView):
    model = CourseInfo
    paginate_by = 8

    def get_queryset(self):
        qs = self.model.objects.all()

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
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk')).count()
        context['quizcount'] = Question.objects.filter(course_code=self.kwargs.get('pk')).count()

        return context


class CourseInfoUpdateView(UpdateView):
    model = CourseInfo
    form_class = CourseInfoForm


class ChapterInfoListView(ListView):
    model = ChapterInfo


class ChapterInfoCreateView(CreateView):
    model = ChapterInfo
    form_class = ChapterInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
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
        # print(request.POST["Use_Flag"])
        if request.POST["Use_Flag"] == 'true':
            Obj.Use_Flag = True
        else:
            Obj.Use_Flag = False
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
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        return context


def CourseForum(request, course):
    course = CourseInfo.objects.get(pk=course)
    course_forum = None
    course_node_forum = None
    try:
        course_node_forum=NodeGroup.objects.get(title='Course')
    except ObjectDoesNotExist:
        NodeGroup.objects.create(title='Course',  description='Root node for course Forum').save()
        course_node_forum=NodeGroup.objects.get(title='Course')

    try:
        course_forum=Topic.objects.get(title=course.Course_Name)
    except ObjectDoesNotExist:
        Topic.objects.create(title=course.Course_Name, node_group=course_node_forum).save()
        course_forum=Topic.objects.get(title=course.Course_Name)
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


class InningInfoCreateView(CreateView):
    model = InningInfo
    form_class = InningInfoForm

class InningInfoDetailView(DetailView):
    model = InningInfo


class InningInfoUpdateView(UpdateView):
    model = InningInfo
    form_class = InningInfoForm


class InningGroupListView(ListView):
    model = InningGroup


class InningGroupCreateView(CreateView):
    model = InningGroup
    form_class = InningGroupForm


class InningGroupCreateAjax(AjaxableResponseMixin, CreateView):
    model = InningGroup
    form_class = InningGroupForm
    template_name = 'ajax/inninggroup_form_ajax.html'


class InningInfoCreateSessionAjax(AjaxableResponseMixin, CreateView):
    model = SessionInfo
    form_class = SessionInfoForm
    template_name = 'ajax/sessioncreate_form_ajax.html'


class InningGroupDetailView(DetailView):
    model = InningGroup


class InningGroupUpdateView(UpdateView):
    model = InningGroup
    form_class = InningGroupForm


class GroupCreateSessionAjax(AjaxableResponseMixin, CreateView):
    model = GroupMapping
    form_class = GroupMappingForm
    template_name = 'ajax/groupcreate_form_ajax.html'


class GroupMappingListView(ListView):
    model = GroupMapping


class GroupMappingCreateView(CreateView):
    model = GroupMapping
    form_class = GroupMappingForm


class GroupMappingDetailView(DetailView):
    model = GroupMapping


class GroupMappingUpdateView(UpdateView):
    model = GroupMapping
    form_class = GroupMappingForm


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
        Obj.Course_Code = CourseInfo.objects.get(pk=request.POST["Course_Code"])
        Obj.Chapter_Code = ChapterInfo.objects.get(id=request.POST["Chapter_Code"])
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = QuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class AssignmentInfoUpdateView(UpdateView):
    model = AssignmentInfo
    form_class = AssignmentInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        return context


class QuestionInfoListView(ListView):
    model = QuestionInfo


class QuestionInfoCreateView(CreateView):
    model = QuestionInfo
    form_class = QuestionInfoForm

    # success_url = 'questioninfo_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


class QuestionInfoCreateViewAjax(AjaxableResponseMixin, CreateView):
    model = QuestionInfo
    form_class = QuestionInfoForm
    template_name = 'ajax/questioninfo_form_ajax.html'

    def post(self, request, *args, **kwargs):
        Obj = QuestionInfo()
        Obj.Question_Title = request.POST["Question_Title"]
        Obj.Question_Score = request.POST["Question_Score"]
        Obj.Question_Description = request.POST["Question_Description"]
        Obj.Answer_Type = request.POST["Answer_Type"]
        Obj.Question_Media_File = request.POST["Question_Media_File"]
        if request.POST["Use_Flag"] == 'true':
            Obj.Use_Flag = True
        else:
            Obj.Use_Flag = False
        Obj.Register_Agent = MemberInfo.objects.get(pk=request.POST["Register_Agent"])
        Obj.Assignment_Code = AssignmentInfo.objects.get(pk=request.POST["Assignment_Code"])
        Obj.save()

        return JsonResponse(
            data={'Message': 'Success'}
        )


class QuestionInfoDetailView(DetailView):
    model = QuestionInfo


class QuestionInfoUpdateView(UpdateView):
    model = QuestionInfo
    form_class = QuestionInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context


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
        context['Question_Code'] = get_object_or_404(QuestionInfo, pk=self.kwargs.get('questioncode'))
        return context


class AssignAnswerInfoDetailView(DetailView):
    model = AssignAnswerInfo


class AssignAnswerInfoUpdateView(UpdateView):
    model = AssignAnswerInfo
    form_class = AssignAnswerInfoForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Question_Code'] = get_object_or_404(QuestionInfo, pk=self.kwargs.get('questioncode'))
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

def chapterviewer(request):
    if request.method == "GET":
        path = settings.MEDIA_ROOT
        chapterID = request.GET['chapterID']
        chapterobj = ChapterInfo.objects.get(id=chapterID)
        courseID = chapterobj.Course_Code.id
        try:
            with open(path + '/chapterBuilder/' + str(courseID) + '/' + str(chapterID) + '/' + str(
                    chapterID) + '.txt') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(e)
        return JsonResponse({'data': data})


def chapterpagebuilder(request, course, chapter):
    chaptertitle = ChapterInfo.objects.get(id=chapter).Chapter_Name
    path = settings.MEDIA_ROOT
    data = None
    try:
        with open(path + '/chapterBuilder/' + str(course) + '/' + str(chapter) + '/' + str(
                chapter) + '.txt') as json_file:
            data = json.load(json_file)
    except Exception as e:
        print(e)
    context = {
        'course': course,
        'chapter': chapter,
        'chaptertitle': chaptertitle,
        'file_path': path,
        'data': data
    }
    return render(request, 'WebApp/chapterbuilder.html', context)


@csrf_exempt
def save_file(request):
    if request.method == "POST":
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        media_type = request.POST['type']
        path = ''
        # for x in range(int(count)):
        if request.FILES['file-0']:
            media = request.FILES['file-0']
            if media_type == 'pic':
                if (media.size/1024) > 2048:
                    return JsonResponse(data = {"message":"File size exceeds 2MB"}, status=500)
            path = settings.MEDIA_ROOT
            # following is commented because filesystemstorage auto create directories if not exist
            # if not os.path.exists(os.path.join(path, 'chapterBuilder')):
            #     os.makedirs(os.path.join(path, 'chapterBuilder'))
            # if not os.path.exists(path+'chapterBuilder/'+courseID):
            #     os.makedirs(os.path.join(path, 'chapterBuilder/'+courseID))
            # if not os.path.exists(path+'chapterBuilder/'+courseID+'/'+chapterID):
            #     os.makedirs(os.path.join(path, 'chapterBuilder/'+courseID+'/'+chapterID))    
            fs = FileSystemStorage(location=path + '/chapterBuilder/' + courseID + '/' + chapterID)
            filename = fs.save(media.name, media)
        return JsonResponse(data={"message": "success"})


@csrf_exempt
def save_json(request):
    if request.method == "POST":
        jsondata = json.loads(request.POST['json'])
        chapterID = request.POST['chapterID']
        courseID = request.POST['courseID']
        path = settings.MEDIA_ROOT
        with open(path + '/chapterBuilder/' + courseID + '/' + chapterID + '/' + chapterID + '.txt', 'w') as outfile:
            json.dump(jsondata, outfile, indent=4)

        chapterObj = ChapterInfo.objects.get(id = chapterID)
        chapterObj.Page_Num = int(jsondata['numberofpages'])
        chapterObj.save()

        return JsonResponse(data = {"message":"Json Saved"})

# -------------------------------------------------------------------------------------------------------
