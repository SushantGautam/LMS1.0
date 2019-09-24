from datetime import datetime

from django.contrib import messages
from django.db import transaction
from django.forms import model_to_dict
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
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

        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')

        # context['surveyForm'] = {'categoryName': list(categoryName)}
        # context['categoryName'] = CategoryInfo.objects.values_list('Category_Name')
        # context['surveyForm'] = serializers.serialize('json', list(categoryName), fields=('Category_Name'))

        return context

    # ......................................Survey Search ..............................................

    def get_queryset(self):
        qs = self.model.objects.filter(Center_Code=self.request.user.Center_Code)
        query = self.request.GET.get('query')
        print(query)
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
#     template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

class SurveyInfo_ajax(AjaxableResponseMixin, CreateView):
    model = SurveyInfo
    form_class = SurveyInfoForm
    template_name = 'ajax/surveyInfoAddSurvey_ajax2.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['questioninfo_formset'] = QuestionInfoFormset(self.request.POST, prefix='questioninfo')  # MCQ
            context['questionansinfo_formset'] = QuestionAnsInfoFormset(self.request.POST,
                                                                        prefix='questionansinfo')  # SAQ
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
        return redirect('surveyinfo_detail', self.object.id)

    def get_form_kwargs(self):
        default_kwargs = super().get_form_kwargs()
        default_kwargs['center_code_id'] = self.request.user.Center_Code.id
        return default_kwargs



from django.forms.models import inlineformset_factory, BaseInlineFormSet


def create_questioninfo_formset(obj_instance):
    class BaseQuestionInfoFormset(BaseInlineFormSet):
        def add_fields(self, form, index):
            super().add_fields(form, index)

            print(form.fields['Question_Name'].initial)
            print(index)

            my_mcqs =obj_instance.questioninfo.all().filter(Question_Type='MCQ')
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

            print(my_data)

                # save the formset in the 'nested' property
            form.nested = OptionInfoFormset(
                instance=form.instance,
                initial = my_op_initial,
                data = form.data if form.is_bound else None,
                files = form.files if form.is_bound else None,
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
    template_name = 'ajax/surveyInfoRetake_ajax.html'

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
            context['categoryObject'] = CategoryInfo.objects.get(id=self.request.GET['categoryId'])
            context['parent_pk'] = obj_instance.pk
        return context

    def get_form_kwargs(self):
        default_kwargs = super().get_form_kwargs()
        default_kwargs['center_code_id'] = self.request.user.Center_Code.id
        return default_kwargs

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
        obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
        self.object.Retaken_From = obj_instance.id
        self.object.Version_No = obj_instance.Version_No + 1
        self.object.save()
        return vform

    def get_initial(self):
        obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
        return model_to_dict(obj_instance,
                             fields=['Survey_Title', 'Start_Date',
                                     'End_Date', 'Center_Code',
                                     'Category_Code', 'Session_code',
                                     'Added_By']
                             )


class CopySurvey(View):
    def get(self):
        oso = SurveyInfo.objects.get(id=self.GET["pk"])
        nso = SurveyInfo.objects.get(id=self.GET["pk"])
        nso.id = None
        nso.save()
        for mcq in oso.questioninfo.all().filter(Question_Type='MCQ'):
            omcq_id = mcq.id
            mcq.id = None
            mcq.Survey_Code = nso
            mcq.save()
            omcq = QuestionInfo.objects.get(id=omcq_id)
            for ops in omcq.optioninfo.all():
                ops.id = None
                ops.Question_Code = mcq
                ops.save()
        for saq in oso.questioninfo.all().filter(Question_Type='SAQ'):
            osaq_id = saq.id
            saq.id = None
            saq.Survey_Code = nso
            saq.save()

        return HttpResponseRedirect(
            reverse(
                'surveyinfo_retake_ajax',
                kwargs={'pk': nso.pk},
            )
        )


# class SurveyInfoRetake_ajax(UpdateView):
#     model = SurveyInfo
#     form_class = SurveyInfoForm
#     template_name = 'ajax/surveyInfoRetake_ajax.html'
#
#     # new_object = None
#
#     # def get_object(self, queryset=None):
#     #     print("oooooooooooooooooooooooooooooo before ooooooooooooooooooooooooooo")
#     #     if self.new_object is None:
#     #         oso = SurveyInfo.objects.get(id=self.kwargs["pk"])
#     #         nso = SurveyInfo.objects.get(id=self.kwargs["pk"])
#     #         nso.id = None
#     #         nso.save()
#     #         for mcq in oso.questioninfo.all().filter(Question_Type='MCQ'):
#     #             omcq_id = mcq.id
#     #             mcq.id = None
#     #             mcq.Survey_Code = nso
#     #             mcq.save()
#     #             omcq = QuestionInfo.objects.get(id=omcq_id)
#     #             for ops in omcq.optioninfo.all():
#     #                 ops.id = None
#     #                 ops.Question_Code = mcq
#     #                 ops.save()
#     #         for saq in oso.questioninfo.all().filter(Question_Type='SAQ'):
#     #             osaq_id = saq.id
#     #             saq.id = None
#     #             saq.Survey_Code = nso
#     #             saq.save()
#     #         print("oooooooooooooooooooooooooooooo new object ooooooooooooooooooooooooooo")
#     #         print(nso.id)
#     #         self.new_object = nso
#     #         return self.new_object
#     #
#     #     else:
#     #         return self.new_object
#
#     def get(self, request, *args, **kwargs):
#         oso = SurveyInfo.objects.get(id=self.kwargs["pk"])
#         nso = SurveyInfo.objects.get(id=self.kwargs["pk"])
#         nso.id = None
#         nso.save()
#         for mcq in oso.questioninfo.all().filter(Question_Type='MCQ'):
#             omcq_id = mcq.id
#             mcq.id = None
#             mcq.Survey_Code = nso
#             mcq.save()
#             omcq = QuestionInfo.objects.get(id=omcq_id)
#             for ops in omcq.optioninfo.all():
#                 ops.id = None
#                 ops.Question_Code = mcq
#                 ops.save()
#         for saq in oso.questioninfo.all().filter(Question_Type='SAQ'):
#             osaq_id = saq.id
#             saq.id = None
#             saq.Survey_Code = nso
#             saq.save()
#         self.kwargs['pk'] = nso.pk
#         return super().get(self, request, *args, **kwargs)
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         print("oooooooooooooooooooooooooooooo self.object ooooooooooooooooooooooooooo")
#         print(self.object.id)
#         if self.request.POST:
#             context['questioninfo_formset'] = QuestionInfoFormset(
#                 self.request.POST,
#                 instance=self.object,
#                 queryset=self.object.questioninfo.all().filter(Question_Type='MCQ').order_by('pk'),
#                 prefix='questioninfo'
#             )  # MCQ
#             context['questionansinfo_formset'] = QuestionAnsInfoFormset(
#                 self.request.POST,
#                 instance=self.object,
#                 queryset=self.object.questioninfo.all().filter(Question_Type='SAQ').order_by('pk'),
#                 prefix='questionansinfo'
#             )  # SAQ
#         else:
#             context['questioninfo_formset'] = QuestionInfoFormset(
#                 instance=self.object,
#                 queryset=self.object.questioninfo.all().filter(Question_Type='MCQ').order_by('pk'),
#                 prefix='questioninfo'
#             )  # MCQ
#             context['questionansinfo_formset'] = QuestionAnsInfoFormset(
#                 instance=self.object,
#                 queryset=self.object.questioninfo.all().filter(Question_Type='SAQ').order_by('pk'),
#                 prefix='questionansinfo'
#             )  # SAQ
#             context['categoryObject'] = CategoryInfo.objects.get(id=self.request.GET['categoryId'])
#         return context
#
#     def form_valid(self, form):
#         # vform = super().form_valid(form)
#
#         # if form.is_valid():
#         #     print("oooooooooooooooooooooooooooooo form_valid ooooooooooooooooooooooooooo")
#         #     self.object = form.save(commit=False)
#         #     print(self.object.id)
#
#         # self.object = form.save(commit=False)
#         # self.object.id = None
#         vform = super().form_valid(form)
#
#         context = self.get_context_data()
#         qn = context['questioninfo_formset']
#         qna = context['questionansinfo_formset']
#         with transaction.atomic():
#             if qn.is_valid():
#                 qn.instance = self.object
#                 qn.save()
#             else:
#                 print(qn.errors)
#                 print('qn is invalid')
#             if qna.is_valid():
#                 qna.instance = self.object
#                 qna.save()
#             else:
#                 print('qna is invalid')
#                 print(qna.errors)
#         obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
#         self.object.Retaken_From = obj_instance.id
#         self.object.Version_No = obj_instance.Version_No + 1
#         self.object.save()
#         return vform
#         # return redirect('surveyinfo_list')


# def get_initial(self):
#     obj_instance = SurveyInfo.objects.get(id=self.kwargs["pk"])
#     return model_to_dict(obj_instance,
#                          fields=['Survey_Title', 'Start_Date',
#                                  'End_Date', 'Center_Code',
#                                  'Category_Code', 'Session_code',
#                                  'Added_By']
#                          )


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
            return SurveyInfo.objects.filter(Category_Code=self.request.GET['categoryId'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['currentDate'] = datetime.now()
        return context

