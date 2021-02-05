from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView

from WebApp.models import MemberInfo, InningInfo, GroupMapping, InningGroup, AssignmentInfo, ChapterInfo, CourseInfo
from event_calendar.forms import CalendarEventForm, CalendarEventUpdateForm
from event_calendar.models import CalendarEvent
from survey.models import SurveyInfo, SubmitSurvey
from django.db.models import Q
 

class EventCreateView(CreateView):
    model = CalendarEvent
    # template_name = 'event_calendar/index.html'
    form_class = CalendarEventForm

    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.register_agent = self.request.user
        self.object.save()
        if self.request.GET.get("return", None) == "json":
            response = {'pk': self.object.pk,
                        'part': self.object.get_participation_type_display(),
                        'type': self.object.get_event_type_display(),
                        }
            return JsonResponse(response)
        else:
            return super().form_valid(form)




class EventUpdateView(UpdateView):
    model = CalendarEvent
    # template_name = 'event_calendar/index.html'
    form_class = CalendarEventUpdateForm

    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)


class EventListView(ListView):
    model = CalendarEvent

    # template_name = "event_calendar/index.html"

    def get_context_data(self):
        context = super().get_context_data()
        datetime_now = timezone.now().replace(microsecond=0)
        users = MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code)
        context['admin_chapter_list'] = ChapterInfo.objects.all()
        
        teacher = MemberInfo.objects.get(pk = self.request.user.pk )
        ingGrp = teacher.inninggroup_set.all()
        course = CourseInfo.objects.filter(inninggroups__in = ingGrp)
        teacher_chapter = ChapterInfo.objects.filter(Course_Code__in = course)
        context['teacher_chapter_list'] = teacher_chapter
     
       
        context['user_list'] = users
        context['r_a'] = CalendarEvent.register_agent
        # context['ev_tp'] = CalendarEvent.event_type
        # print('Type:', context['ev_tp'])

        s_list = InningInfo.objects.filter(Use_Flag=True,
                                                       Start_Date__lte=datetime_now,

                                                       End_Date__gte=datetime_now,
                                                       Course_Group__Teacher_Code=self.request.user.pk).distinct()


        context['session'] = s_list
       
       


        if self.request.user.Is_Student:

            batches = GroupMapping.objects.filter(Students__id=self.request.user.id, Center_Code=self.request.user.Center_Code)
            sessions = []
            if batches:
                for batch in batches:
                    # Filtering out only active sessions
                    session = InningInfo.objects.filter(Groups__id=batch.id, End_Date__gt=datetime_now)
                    sessions += session
            courses = set()
            activeassignments = []
            print("Sessions", sessions)
            if sessions:
                for session in sessions:
                    course = session.Course_Group.all()
                    courses.update(course)
                print("Course", courses)
                for course in courses:
                    activeassignments += AssignmentInfo.objects.filter(
                        Course_Code=course.Course_Code.id, Chapter_Code__Use_Flag=True)[:7]

            student_group = self.request.user.groupmapping_set.all()
            student_session = InningInfo.objects.filter(Groups__in=student_group)
            active_student_session = InningInfo.objects.filter(Groups__in=student_group, End_Date__gt=datetime_now)
            student_course = InningGroup.objects.filter(inninginfo__in=active_student_session).values("Course_Code")

            # Predefined category name "general, session, course, system"
            general_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="general",
                                                       Center_Code=self.request.user.Center_Code, Use_Flag=True)
            session_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="session",
                                                       Session_Code__in=student_session, Use_Flag=True)
            course_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="course",
                                                      Course_Code__in=student_course, Use_Flag=True)
            system_survey = SurveyInfo.objects.filter(Category_Code__Category_Name__iexact="system", Use_Flag=True)


            my_queryset = None
            my_queryset = general_survey | session_survey | course_survey | system_survey
            # my_queryset = my_queryset.filter(End_Date__gt=timezone.now(), Survey_Live=False)
            my_queryset = my_queryset.filter(End_Date__gt=timezone.now())
            context['activeassignments'] = activeassignments
            context['activesurvey'] = my_queryset
            submitSurveyQuerySet = SubmitSurvey.objects.filter(
                Student_Code=self.request.user.id)
            context['submittedSurvey'] = [
                el.Survey_Code.id for el in submitSurveyQuerySet]
            # context['is_submitted'] = SubmitSurvey.objects.filter(Survey_Code=self.object.id,
            #                                                       Student_Code=self.request.user.id).exists()
            print("ActiveAssignment",activeassignments)
        


        context['daily_event']=context['object_list'].filter(Q(repeat_type='DA')| Q(repeat_type="WE"))
        context['monthly_event']=context['object_list'].filter(repeat_type='MO')
        context['weekday_event']=context['object_list'].filter(repeat_type='WD')
        return context

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        return queryset.filter(register_agent__Center_Code=self.request.user.Center_Code)


class EventDeleteView(DeleteView):
    model = CalendarEvent
    form_class = CalendarEventUpdateForm
    # template_name = 'event_calendar/index.html'
    # success_url = reverse_lazy('event_calendar')


class EventUpdatedView(UpdateView):
    model = CalendarEvent
    # template_name = 'event_calendar/index.html'
    form_class = CalendarEventForm

    # success_url = reverse_lazy('event_calendar')

    def form_invalid(self, form):
        print(form.errors)
        raise Exception
        return super().form_invalid(form)

