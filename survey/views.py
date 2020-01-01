from datetime import datetime, timedelta

from django import forms
from django.contrib import messages
from django.core import serializers
from django.db import transaction
from django.db.models import Q
from django.forms import model_to_dict
from django.forms.models import inlineformset_factory, BaseInlineFormSet
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, UpdateView, CreateView
from django.views.generic.base import View

from .forms import CategoryInfoForm, SurveyInfoForm, QuestionInfoForm, OptionInfoForm, SubmitSurveyForm, AnswerInfoForm, \
    QuestionInfoFormset, QuestionAnsInfoFormset
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo


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


class CategoryInfoListView(ListView):
    model = CategoryInfo


class CategoryInfoCreateView(CreateView):
    model = CategoryInfo
    form_class = CategoryInfoForm


class CategoryInfoDetailView(DetailView):
    model = CategoryInfo


class CategoryInfoUpdateView(UpdateView):
    model = CategoryInfo
    form_class = CategoryInfoForm


class SurveyList(ListView):
    model = SurveyInfo

    # ....................................Pagination.............................................................

    # def listing(request):
    #     survey_list = SurveyInfo.objects.all()
    #     print(survey_list)
    #     print('keep going')
    #     paginator = Paginator(survey_list, 10)  # Show 10 contacts per page
    #
    #     page = request.GET.get('page')
    #     surveys = paginator.get_page(page)
    #     print(surveys)
    #     return render(request, 'surveyinfo_expireView.html', {'surveys': surveys})


class SurveyInfoListView(ListView):
    model = SurveyInfo
    template_name = 'survey/surveylist.html'

    paginate_by = 6

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.GET = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now().date()
        context['categories'] = CategoryInfo.objects.all()
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()

        return context
        # context['']

        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')

        # context['surveyForm'] = {'categoryName': list(categoryName)}
        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')
        # context['surveyForm'] = serializers.serialize('json', list(categoryName), fields=('Category_Name'))

    # ......................................Survey Search ..............................................

    def get_queryset(self):
        qs = self.model.objects.filter(Center_Code=self.request.user.Center_Code)
        query = self.request.GET.get('query')
        if query:
            query = query.strip()
            qs = qs.filter(Survey_Title__contains=query)
            if not len(qs):
                messages.error(self.request, 'Sorry no course found! Try with a different keyword')
        qs = qs.order_by("-id")  # you don't need this if you set up your ordering on the model
        return qs

    # def post(self, request):
    #     obj = SurveyInfo()
    #     if request.method == "POST":
    #         obj.Survey_Title = request.POST['Survey_Title']
    #         obj.Start_Date = request.POST['Start_Date']
    #         obj.End_Date = request.POST['End_Date']
    #         obj.Session_Code = InningInfo.objects.get(pk = request.POST['Session_Code'])
    #         obj.Course_Code = CourseInfo.objects.get(pk = request.POST['Course_Code'])
    #         obj.save()
    #         print(obj.id)
    #     return redirect('surveyinfo_detail', obj.id)


# def get_context_data(self, **kwargs):
#     categoryName = CategoryInfo.objects.filter(code__startswith='a').values_list('Category_Name')
#     return JsonResponse({'categoryName': list(categoryName)})

# def get_survey_info(request):
#     id = request.GET.get('id', None)
#     # questions = QuestionInfo.objects.filter(
#     #     Survey_Code=id).order_by('pk')
#     options = OptionInfo.objects.all()
#     data = {'options':options}
#     print(data)
#     #submit = SubmitSurvey.objects.all()
#     # context = 'asdasdasdasd'
#     return JsonResponse(data)


class SurveyInfoCreateView(CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm


# class SurveyInfo_ajax(AjaxableResponseMixin, CreateView):
#     model = SurveyInfo
#     form_class = SurveyInfoForm
#     template_name = 'ajax/surveyInfoAddSurvey_ajax2.html

class SurveyInfo_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_form_kwargs(self):
        kwargs = super(SurveyInfo_ajax, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST, prefix='questioninfo')  # MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST,
                                                                        prefix='questionansinfo')  # SAQ
        else:
            context['questioninfo_formset'] = QuestionInfoFormset(prefix='questioninfo')
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(prefix='questionansinfo')
            context['category_name'] = self.request.GET['category_name']
            if self.request.GET['category_name'] == "Session":
                context['form']['Session_Code'].initial = self.request.GET['Session_Code']
        return context

    def form_valid(self, form):
        # vform = super().form_valid(form)
        if form.is_valid():
            self.object = form.save(commit=False)
            if self.request.GET['category_name'].lower() == "system":
                self.object.Center_Code = self.request.user.Center_Code
            else:
                self.object.Center_Code = self.request.user.Center_Code
            self.object.Added_By = self.request.user
            self.object.save()
            if self.request.GET['category_name'].lower() == "live":
                self.object.Survey_Live = True
                self.object.End_Date = timezone.now() + timedelta(seconds=int(self.request.POST["End_Time"]))
                self.object.save()
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            # else:
            #     print(qn.errors)
            #     print('qn is invalid')
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
            # else:
            #     print('qna is invalid')
            #     print(qna.errors)
        response = {'url': self.request.build_absolute_uri(reverse('surveyinfo_detail', kwargs={'pk': self.object.id})),
                    'teacher_url': self.request.build_absolute_uri(
                        reverse('surveyinfodetail', kwargs={'pk': self.object.id})),
                    'student_url': self.request.build_absolute_uri(
                        reverse('questions_student_detail', kwargs={'pk': self.object.id}))}
        return JsonResponse(response)


def create_questioninfo_formset(obj_instance):
    class BaseQuestionInfoFormset(BaseInlineFormSet):
        def add_fields(self, form, index):
            super().add_fields(form, index)

            # print(form.fields['Question_Name'].initial)
            # print(index)
            form.fields['Question_Type'].initial = "MCQ"
            form.fields['Question_Type'].widget = forms.HiddenInput()
            my_mcqs = obj_instance.questioninfo.all().filter(Question_Type='MCQ')
            if form.is_bound:
                my_op_initial = None
            elif index is not None:
                my_op_initial = [my_dict for my_dict in my_mcqs[index].optioninfo.all().values()]
            else:
                my_op_initial = None
            OptionInfoFormset = inlineformset_factory(
                QuestionInfo,
                OptionInfo,
                fields=('Option_Name',),
                can_delete=False,
                extra=len(my_op_initial) if my_op_initial is not None else 0,
            )
            if form.is_bound:
                my_data = form.data
            elif form.fields['Question_Name'] is not None:
                my_data = form.data
            else:
                my_data = None

            # print(my_data)

            # save the formset in the 'nested' property
            form.nested = OptionInfoFormset(
                instance=form.instance,
                initial=my_op_initial,
                data=form.data if form.is_bound else None,
                files=form.files if form.is_bound else None,
                prefix='optioninfo-%s-%s' % (
                    form.prefix,
                    OptionInfoFormset.get_default_prefix()),
            )

        def is_valid(self):
            result = super().is_valid()

            if self.is_bound:
                for form in self.forms:
                    if hasattr(form, 'nested'):
                        result = result and form.nested.is_valid()

            return result

        def save(self, commit=True):

            result = super().save(commit=commit)

            for form in self.forms:
                if hasattr(form, 'nested'):
                    if not self._should_delete_form(form):
                        form.nested.save(commit=commit)

            return result

    return BaseQuestionInfoFormset


class SurveyInfoRetake_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_form_kwargs(self):
        kwargs = super(SurveyInfoRetake_ajax, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        kwargs.update({'object': SurveyInfo.objects.get(id=self.kwargs["pk"])})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])

        my_mcq_initial = [my_dict for my_dict in obj_instance.questioninfo.all().filter(Question_Type='MCQ').values()]
        my_saq_initial = [my_dict for my_dict in obj_instance.questioninfo.all().filter(Question_Type='SAQ').values()]

        SaqFormSet = inlineformset_factory(
            SurveyInfo,
            QuestionInfo,
            extra=len(my_saq_initial),
            fields=('Question_Name', 'Question_Type'),
        )
        McqFormSet = inlineformset_factory(
            SurveyInfo,
            QuestionInfo,
            formset=create_questioninfo_formset(obj_instance),
            extra=len(my_mcq_initial),
            fields=('Question_Name', 'Question_Type'),
        )

        if self.request.POST:
            context['questioninfo_formset'] = McqFormSet(
                self.request.POST,
                prefix='questioninfo'
            )  # MCQ
            context['questionansinfo_formset'] = SaqFormSet(
                self.request.POST,
                prefix='questionansinfo'
            )  # SAQ
        else:
            context['questioninfo_formset'] = McqFormSet(
                # instance=obj_instance,
                # queryset=QuestionInfo.objects.filter(Question_Type='MCQ'),
                initial=my_mcq_initial,
                prefix='questioninfo'
            )  # MCQ
            context['questionansinfo_formset'] = SaqFormSet(
                # instance=obj_instance,
                # queryset=QuestionInfo.objects.filter(Question_Type='MCQ'),
                initial=my_saq_initial,
                prefix='questionansinfo'
            )  # SAQ
            context['category_name'] = self.request.GET['category_name']
            context['parent_pk'] = obj_instance.pk
        return context

    def form_valid(self, form):
        obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
        if form.is_valid():
            self.object = form.save(commit=False)
            self.object.Center_Code = obj_instance.Center_Code
            self.object.Added_By = self.request.user
            self.object.save()
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            # else:
            #     print(qn.errors)
            #     print('qn is invalid')
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
            # else:
            #     print('qna is invalid')
            #     print(qna.errors)
        if obj_instance.Retaken_From:
            self.object.Retaken_From = obj_instance.Retaken_From
        else:
            self.object.Retaken_From = self.kwargs["pk"]
        self.object.Version_No = obj_instance.Version_No + 1
        self.object.save()
        # check the request path and redirect as the value of path
        # if 'teachers' in self.request.path:
        #     return redirect('surveyinfodetail', self.object.id)
        # else:
        #     return redirect('surveyinfo_detail', self.object.id)
        response = {'url': self.request.build_absolute_uri(reverse('surveyinfo_detail', kwargs={'pk': self.object.id})),
                    'teacher_url': self.request.build_absolute_uri(
                        reverse('surveyinfodetail', kwargs={'pk': self.object.id})),
                    'student_url': self.request.build_absolute_uri(
                        reverse('questions_student_detail', kwargs={'pk': self.object.id}))}
        return JsonResponse(response)

    def get_initial(self):
        obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
        return model_to_dict(obj_instance,
                             fields=['Survey_Title', 'Start_Date',
                                     'End_Date', 'Center_Code',
                                     'Category_Code', 'Session_code',
                                     'Added_By']
                             )


class SurveyInfoDetailView(DetailView):
    model = SurveyInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')
        context['options'] = OptionInfo.objects.filter(Question_Code__in=context['questions']).order_by('pk')
        context['submit'] = SubmitSurvey.objects.filter(Survey_Code=self.kwargs.get('pk')).count()
        if self.object.Retaken_From:
            context['history'] = SurveyInfo.objects.filter(id=self.object.Retaken_From)
            context['history'] |= SurveyInfo.objects.filter(Retaken_From=self.object.Retaken_From).order_by(
                'Version_No')

        else:
            context['history'] = SurveyInfo.objects.filter(id=self.object.id)
            context['history'] |= SurveyInfo.objects.filter(Retaken_From=self.object.id).order_by(
                'Version_No')
        return context


class liveProgressResult(View):
    def get(self, request, *args, **kwargs):
        survey_obj = SurveyInfo.objects.get(pk=self.kwargs['pk'])
        questions = QuestionInfo.objects.filter(Survey_Code=survey_obj.id)
        options = OptionInfo.objects.filter(Question_Code__in=questions)

        for x in options:
            total_answers = x.Question_Code.answerinfo.all().count()
            total_selected = x.Question_Code.answerinfo.filter(Answer_Value=x.id).count()

            if total_answers != 0:
                x.Vote_Count = (total_selected * 100) / total_answers
            else:
                x.Vote_Count = 0
        Participants = SubmitSurvey.objects.filter(Survey_Code=survey_obj.id).count()
        data = serializers.serialize("json", options)
        return JsonResponse([data, Participants], safe=False)


class SurveyInfoUpdateView(UpdateView):
    model = SurveyInfo
    form_class = SurveyInfoForm


# def surveyinfo_category(request, id):
#     category = SurveyInfo.objects.filter(Category_Name)
#     return JsonResponse({'category': 'category'})


class QuestionInfoListView(ListView):
    model = QuestionInfo


class QuestionInfoCreateView(CreateView):
    model = QuestionInfo
    form_class = QuestionInfoForm


class QuestionInfoDetailView(DetailView):
    model = QuestionInfo


class QuestionInfoUpdateView(UpdateView):
    model = QuestionInfo
    form_class = QuestionInfoForm


class OptionInfoListView(ListView):
    model = OptionInfo


class OptionInfoCreateView(CreateView):
    model = OptionInfo
    form_class = OptionInfoForm


class OptionInfoDetailView(DetailView):
    model = OptionInfo


class OptionInfoUpdateView(UpdateView):
    model = OptionInfo
    form_class = OptionInfoForm


class SubmitSurveyListView(ListView):
    model = SubmitSurvey


class SubmitSurveyCreateView(CreateView):
    model = SubmitSurvey
    form_class = SubmitSurveyForm


class SubmitSurveyDetailView(DetailView):
    model = SubmitSurvey


class SubmitSurveyUpdateView(UpdateView):
    model = SubmitSurvey
    form_class = SubmitSurveyForm


class AnswerInfoListView(ListView):
    model = AnswerInfo


class AnswerInfoCreateView(CreateView):
    model = AnswerInfo
    form_class = AnswerInfoForm


class AnswerInfoDetailView(DetailView):
    model = AnswerInfo


class AnswerInfoUpdateView(UpdateView):
    model = AnswerInfo
    form_class = AnswerInfoForm


class surveyFilterCategory(ListView):
    model = SurveyInfo
    template_name = 'survey/common/surveyinfo_expireView.html'

    paginate_by = 6

    def get_queryset(self):
        category_name = self.request.GET['category_name'].lower()
        date_filter = self.request.GET['date_filter'].lower()
        print("category id:", category_name)
        print("date filter:", date_filter)
        my_queryset = SurveyInfo.objects.filter(
            Q(Center_Code=None) | Q(Center_Code=self.request.user.Center_Code))
        print("all survey query", len(my_queryset))
        if category_name != "all_survey":
            my_queryset = my_queryset.filter(Category_Code__Category_Name__iexact=category_name)
            print(category_name, "query", len(my_queryset))
        if date_filter == "active":
            my_queryset = my_queryset.filter(End_Date__gt=timezone.now(), Survey_Live=False)
            print(date_filter, "query", len(my_queryset))
        elif date_filter == "expire":
            my_queryset = my_queryset.filter(End_Date__lte=timezone.now())
            print(date_filter, "query", len(my_queryset))
        elif date_filter == "live":
            my_queryset = my_queryset.filter(End_Date__gt=timezone.now(), Survey_Live=True)
            print(date_filter, "query", len(my_queryset))

        return my_queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        context['category_name'] = self.request.GET['category_name'].lower()
        context['date_filter'] = self.request.GET['date_filter'].lower()
        return context

    # ....................................Pagination.............................................................

    # def listing(request):
    #     survey_list = SurveyInfo.objects.all()
    #     print(survey_list)
    #     paginator = Paginator(survey_list, 10)
    #
    #     page = request.GET.get('page')
    #     surveys = paginator.get_page(page)
    #     print(surveys)
    #     return render(request, 'surveyinfo_expireView.html', {'surveys': surveys})


def SurveyclearViewForAdmin(request, pk):
    filteredSubmitSurvey = SubmitSurvey.objects.filter(Survey_Code=pk)
    filteredAnswerInfo = AnswerInfo.objects.filter(Submit_Code__in=filteredSubmitSurvey).delete()
    filteredSubmitSurvey.delete()
    messages.add_message(request, messages.SUCCESS,
                         'All submitted contents in this survey Deleted Successfully.')

    return redirect('surveyinfo_detail', pk=pk)
