from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, UpdateView, CreateView

from .forms import CategoryInfoForm, SurveyInfoForm, QuestionInfoForm, OptionInfoForm, SubmitSurveyForm, AnswerInfoForm, \
    QuestionInfoFormset, QuestionAnsInfoFormset
from .models import CategoryInfo, SurveyInfo, QuestionInfo, OptionInfo, SubmitSurvey, AnswerInfo
from datetime import datetime

from django.db import transaction
from django.http import JsonResponse
from django.views.generic import DetailView, ListView, UpdateView, CreateView

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


class SurveyInfoListView(ListView):
    model = SurveyInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now().date()
        context['categories'] = CategoryInfo.objects.all()
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')

        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()
        return context

class SurveyInfoCreateView(CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm

# class SurveyInfo_ajax(AjaxableResponseMixin, CreateView):
#     model = SurveyInfo
#     form_class = SurveyInfoForm
#     template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

class SurveyInfo_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST, prefix='questioninfo') #MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST, prefix='questionansinfo') #SAQ
        else:
            context['questioninfo_formset'] = QuestionInfoFormset(prefix='questioninfo')
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(prefix='questionansinfo')
            context['categoryObject'] = CategoryInfo.objects.get(id=self.request.GET['categoryId'])
        return context
    
    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            else:
                print(qn.errors)
                print('qn is invalid')
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
            else:
                print('qna is invalid')
                print(qna.errors)
        return vform


class SurveyInfoRetake_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.kwargs["survey_id"])
        obj_instance = SurveyInfo.objects.get(id=self.kwargs["survey_id"])
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST,
                                                                  queryset=QuestionInfo.objects.filter(
                                                                      Question_Type="MCQ"),
                                                                  instance=obj_instance,
                                                                  prefix='questioninfo')  # MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST,
                                                                        queryset=QuestionInfo.objects.filter(
                                                                            Question_Type="SAQ"),
                                                                        instance=obj_instance,
                                                                        prefix='questionansinfo')  # SAQ
        else:
            context['questioninfo_formset'] = QuestionInfoFormset(instance=obj_instance,
                                                                  queryset=QuestionInfo.objects.filter(
                                                                      Question_Type="MCQ"),
                                                                  prefix='questioninfo')
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(instance=obj_instance,
                                                                        queryset=QuestionInfo.objects.filter(
                                                                            Question_Type="SAQ"),
                                                                        prefix='questionansinfo')
            context['categoryObject'] = CategoryInfo.objects.get(id=self.request.GET['categoryId'])
        return context

    def form_valid(self, form):
        vform = super().form_valid(form)
        context = self.get_context_data()
        qn = context['questioninfo_formset']
        qna = context['questionansinfo_formset']
        with transaction.atomic():
            if qn.is_valid():
                qn.instance = self.object
                qn.save()
            else:
                print(qn.errors)
                print('qn is invalid')
            if qna.is_valid():
                qna.instance = self.object
                qna.save()
            else:
                print('qna is invalid')
                print(qna.errors)
        return vform

class SurveyInfoDetailView(DetailView):
    model = SurveyInfo

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = QuestionInfo.objects.filter(
            Survey_Code=self.kwargs.get('pk')).order_by('pk')
        context['options'] = OptionInfo.objects.all()
        context['submit'] = SubmitSurvey.objects.all()
        return context


# class liveProgressResult(AjaxableResponseMixin, View):
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#
#         return render(request, template_name, context=None

class SurveyInfoUpdateView(UpdateView):
    model = SurveyInfo
    form_class = SurveyInfoForm


def surveyinfo_category(request, id):
    category = SurveyInfo.objects.filter(Category_Name)
    return JsonResponse({'category': 'category'})


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
    template_name = 'survey/surveyinfo_expireView.html' 

    def get_queryset(self):
        if self.request.GET['categoryId'] == '0':
            return SurveyInfo.objects.all()
        else:
            return SurveyInfo.objects.filter(Category_Code = self.request.GET['categoryId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        return context