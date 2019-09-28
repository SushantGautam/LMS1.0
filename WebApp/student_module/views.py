# from django.shortcuts import render
#
#
# def start(request):
#     """Start page with a documentation.
#     """
#     # return render(request,"start.html")
#     return render(request, "student_module/homepage.html")

from datetime import datetime

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordContextMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
# Create your views here.
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormView

from WebApp.forms import UserUpdateForm
from WebApp.models import CourseInfo, GroupMapping, InningInfo, ChapterInfo, AssignmentInfo, MemberInfo, \
    AssignmentQuestionInfo, \
    AssignAnswerInfo
from quiz.models import Question, Quiz
from survey.models import SurveyInfo, CategoryInfo, OptionInfo, SubmitSurvey, AnswerInfo, QuestionInfo

datetime_now = datetime.now()


def start(request):
    if request.user.Is_Student:
        batches = GroupMapping.objects.filter(Students__id=request.user.id, Center_Code=request.user.Center_Code)
        sessions = []
        if batches:
            for batch in batches:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id,End_Date__gt=datetime_now)
                sessions += session
        courses = set()
        activeassignments = []   
        if sessions:
            for session in sessions:
                course = session.Course_Group.all()
                courses.update(course)
        
            for course in courses:
                activeassignments += AssignmentInfo.objects.filter(Assignment_Deadline__gte=datetime_now)[:7]
 
        
        return render(request, 'student_module/dashboard.html',
                      {'GroupName': batches, 'Group': sessions, 'Course': courses,'activeAssignments':activeassignments})




class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('student_user_profile')
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


def student_editprofile(request):
    if not request.user.is_authenticated:
        return HttpResponse("you are not authenticated", {'error_message': 'Error Message Customize here'})
    post = get_object_or_404(MemberInfo, pk=request.user.id)
    if request.method == "POST":

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            post.date_last_update = datetime.now()
            post.save()
            return redirect('student_user_profile')
    else:

        form = UserUpdateForm(request.POST, request.FILES, instance=post)

    return render(request, 'student_module/editprofile.html', {'form': form})


def quiz(request):
    return render(request, 'student_module/quiz.html')


def quizzes(request):
    return render(request, 'student_module/quizzes.html')


def calendar(request):
    return render(request, 'student_module/calendar.html')

class MyCoursesListView(ListView):
    model = CourseInfo
    template_name = 'student_module/myCourse.html'

    paginate_by = 8

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['batches'] = GroupMapping.objects.filter(Students__id=self.request.user.id, Center_Code=self.request.user.Center_Code)

        sessions = []
        if context['batches']:
            for batch in context['batches']:
                # Filtering out only active sessions
                session = InningInfo.objects.filter(Groups__id=batch.id,End_Date__gt=datetime_now)
                sessions += session
        context['sessions'] = sessions
        courses = set()
        if context['sessions']:
            for session in context['sessions']:
                course = session.Course_Group.all()
                courses.update(course)
        context['Course'] = courses

        return context

    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('mycoursequery')
        if query:
            query=query.strip()
            qs = qs.filter(Course_Name__contains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs


class MyAssignmentsListView(ListView):
    model = AssignmentInfo
    template_name = 'student_module/myassignments_list.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['GroupName'] = []
        context['GroupName'] += GroupMapping.objects.filter(Students__id=self.request.user.id)
              
        context['Group'] = []
        for group in context['GroupName']:
            context['Group'] += InningInfo.objects.filter(Groups__id=group.id)
        context['Course'] = []
        for course in context['Group']:
            context['Course'] = course.Course_Group.all()

        return context


class CourseInfoListView(ListView):
    model = CourseInfo
    template_name = 'student_module/courseinfo_list.html'
    
    paginate_by = 8


    def get_queryset(self):
        qs = self.model.objects.all()

        query = self.request.GET.get('coursequery')
        if query:
            query = query.strip()
            qs = qs.filter(Course_Name__contains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs

class CourseInfoDetailView(DetailView):
    model = CourseInfo
    template_name = 'student_module/courseinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['chapters'] = ChapterInfo.objects.filter(Course_Code=self.kwargs.get('pk')).order_by('Chapter_No')
        context['surveycount'] = SurveyInfo.objects.filter(Course_Code=self.kwargs.get('pk'))
        context['quizcount'] = Question.objects.filter(course_code=self.kwargs.get('pk'))
        return context


class ChapterInfoListView(ListView):
    model = ChapterInfo


class ChapterInfoDetailView(DetailView):
    model = ChapterInfo
    template_name = 'student_module/chapterinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['assignments'] = AssignmentInfo.objects.filter(Chapter_Code=self.kwargs.get('pk'))
        context['post_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), draft=False, post_test=True)
        context['pre_quizes'] = Quiz.objects.filter(chapter_code=self.kwargs.get('pk'), draft=False, pre_test=True)

        return context


class AssignmentInfoDetailView(DetailView):
    model = AssignmentInfo
    template_name = 'student_module/assignmentinfo_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Questions'] = AssignmentQuestionInfo.objects.filter(Assignment_Code=self.kwargs.get('pk'))
        context['Course_Code'] = get_object_or_404(CourseInfo, pk=self.kwargs.get('course'))
        context['Chapter_No'] = get_object_or_404(ChapterInfo, pk=self.kwargs.get('chapter'))
        context['Answers'] = []
        AnsweredQuestion = set()
        Question = set()

        for question in context['Questions']:
            Answer = AssignAnswerInfo.objects.filter(Student_Code=self.request.user.pk,Question_Code=question.id)
            context['Answers']+= Answer
            Question.add(question.id)
        # print (context['Answers'])
        for answers in context['Answers']:
            # print (answers.Question_Code.id)
            AnsweredQuestion.add(answers.Question_Code.id)
        # print(Question)
        # print(context['AnsweredQuestion'])
        context['notAnswered'] = Question - AnsweredQuestion
        print(context['notAnswered'])
        # context['Assignment_Code'] = get_object_or_404(AssignmentInfo, pk=self.kwargs.get('assignment'))
        return context

class submitAnswer(View):
    model = AssignAnswerInfo()


    def post(self, request, *args, **kwargs):
        Obj = AssignAnswerInfo()
        Obj.Assignment_Answer = request.POST["Assignment_Answer"]
        Obj.Student_Code = MemberInfo.objects.get(pk=request.POST["Student_Code"])
        Obj.Question_Code = AssignmentQuestionInfo.objects.get(pk=request.POST["Question_Code"])
        print(Obj.Student_Code)
        Obj.save()
       
        return JsonResponse(
            data={'Message': 'Success'}
        )

def ProfileView(request):
    return render(request, 'student_module/profile.html')


# def questions_student(request):
#     return render(request, 'student_module/questions_student.html')

class questions_student(ListView):
    model = SurveyInfo
    template_name = 'student_module/questions_student.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now().date()
        context['categories'] = CategoryInfo.objects.all()

        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        
        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')

        # context['surveyForm'] = {'categoryName': list(categoryName)}
        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')
        # context['surveyForm'] = serializers.serialize('json', list(categoryName), fields=('Category_Name'))
        

        return context

class questions_student_detail(DetailView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        return context

class questions_student_detail_history(DetailView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_detail_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        return context


class ParticipateSurvey(View):

    def post(self, request, *args, **kwargs):
        surveyId = request.POST["surveyInfoId"]
        userId = self.request.user.id
        # print(request.POST)
        submitSurvey = SubmitSurvey()
        submitSurvey.Survey_Code = SurveyInfo.objects.get(id = surveyId)
        submitSurvey.Student_Code = MemberInfo.objects.get(id = userId)
        submitSurvey.save()

        for question in QuestionInfo.objects.filter(Survey_Code = surveyId):

            optionId = request.POST[str(question.id)]
            answerObject = AnswerInfo()
            answerObject.Answer_Value = optionId
            answerObject.Question_Code = question
            answerObject.Submit_Code = submitSurvey
            answerObject.save()
    
        return redirect('questions_student')


class surveyFilterCategory_student(ListView):
    model = SurveyInfo
    template_name = 'student_module/questions_student_listView.html'

    def get_queryset(self):
        # print(self.request.GET['categoryId'])
        # print(SurveyInfo.objects.filter(Category_Code = self.request.GET['categoryId']))
        if self.request.GET['categoryId'] == '0':

            return SurveyInfo.objects.all()
            # filter(Center_Code = self.request.user.Center_Code)
        else:
            return SurveyInfo.objects.filter(Category_Code=self.request.GET['categoryId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()

        submitSurveyQuerySet = SubmitSurvey.objects.filter(Student_Code=self.request.user.id)
        context['submittedSurvey'] = [el.Survey_Code.id for el in submitSurveyQuerySet]

        return context

