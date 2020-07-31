from WebApp.models import MemberInfo
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from .forms import DraftUpdateForm, MailForm, ReplyForm

from mail.models import Mail
from mail.models import MailReceiver


class MailListView(ListView):
    model = MailReceiver
    paginate_by = 10
    template_name = 'mail/index.html'

    def get_queryset(self):
        queryset = MailReceiver.objects.order_by('-received_date')
        # queryset = queryset.filter(Q(receiver=self.request.user) | Q(mail__sender=self.request.user))
        email_type = self.request.GET.get('email_type', "inbox")
        if email_type == "inbox":
            queryset = queryset.filter(Q(receiver=self.request.user) & Q(mail_deleted=False) & Q(mail_spam=False))

        if email_type == "received_starred":
            queryset = queryset.filter(
                receiver=self.request.user, mail_deleted=False, mail_starred=True, mail_spam=False)
        # if email_type == "starred":
        #   queryset = queryset.filter(
        #     Q(receiver=self.request.user) & Q(mail_deleted=False) & Q(mail_starred=True) & Q(mail_spam=False))
        if email_type == "spam":
            queryset = queryset.filter(Q(receiver=self.request.user) & Q(mail_deleted=False) & Q(mail_spam=True))
        if email_type == "received_trash":
            queryset = queryset.filter(Q(receiver=self.request.user) | Q(mail__sender=self.request.user))
            queryset = queryset.filter(mail_deleted=True)
        queryset = queryset.filter(receiver=self.request.user)
        if email_type == "general":
            queryset = queryset.filter(mail__label='GR')
        if email_type == "support":
            queryset = queryset.filter(mail__label='SP')
        if email_type == "assignment":
            queryset = queryset.filter(mail__label='AS')
        if email_type == "exam":
            queryset = queryset.filter(mail__label='EX')
        if email_type == "practical":
            queryset = queryset.filter(mail__label='PR')

        search = self.request.GET.get('search', "")
        queryset = queryset.filter(Q(mail__sender__username__icontains=search) | Q(mail__body__icontains=search) | Q(
            mail__subject__icontains=search))
        filter_type = self.request.GET.get('filter', "date")
        if filter_type == "date":
            queryset = queryset.order_by('-received_date')
        if filter_type == "from":
            queryset = queryset.order_by('mail__sender__username')
        if filter_type == "subject":
            queryset = queryset.order_by('mail__subject')
        if filter_type == "UnRead":
            queryset = queryset.order_by('mail_viewed')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_list'] = MemberInfo.objects.filter(
            Center_Code=self.request.user.Center_Code
        ).exclude(id=self.request.user.id)
        context['label_list'] = Mail.LABEL_CHOICES
        context['email_type'] = self.request.GET.get('email_type', "inbox")
        context['inbox_count'] = MailReceiver.objects.filter(receiver=self.request.user, mail_deleted=False,
                                                             mail_spam=False, mail_viewed=False).count()
        context['starred_count'] = MailReceiver.objects.filter(Q(mail_starred=True, mail_deleted=False,
                                                                 mail_spam=False, receiver=self.request.user) | Q(
            mail__sender_starred=True, mail__sender_delete=False,
            mail__sender=self.request.user)).count()
        context['starred_count'] = MailReceiver.objects.filter(mail_starred=True, mail_deleted=False,
                                                               receiver=self.request.user).count()
        context['trash_count'] = MailReceiver.objects.filter(mail_deleted=True, receiver=self.request.user).count()
        context['search_q'] = self.request.GET.get('search', '')
        context['filter'] = self.request.GET.get('filter', '')
        context['glc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='GR').count()
        context['slc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='SP').count()
        context['alc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='AS').count()
        context['elc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='EX').count()
        context['plc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='PR').count()
        return context


class MailDraftView(ListView):
    model = Mail
    paginate_by = 10
    template_name = "mail/index.html"

    def get_queryset(self):
        email_type = self.request.GET.get('email_type', "send")
        queryset = Mail.objects.order_by('-created_date').filter(sender_delete_p=False)
        if email_type == "send":
            queryset = queryset.filter(sender=self.request.user, reply_to__isnull=True)
            queryset = queryset.filter(sender_delete=False, mail_draft=False)
        if email_type == "draft":
            queryset = queryset.filter(sender=self.request.user)
            queryset = queryset.filter(mail_draft=True, sender_delete=False)
        if email_type == "outbox_delete":
            queryset = queryset.filter(sender=self.request.user, reply_to__isnull=True, sender_delete=True)

        if email_type == "starred_outbox":
            queryset = queryset.filter(sender=self.request.user, reply_to__isnull=True, sender_delete=False,
                                       sender_starred=True)

        search = self.request.GET.get('search', "")
        queryset = queryset.filter(Q(sender__username__icontains=search) | Q(body__icontains=search) | Q(
            subject__icontains=search))
        filter_type = self.request.GET.get('filter', "date")
        if filter_type == "date":
            queryset = queryset.order_by('-created_date')

        if filter_type == "subject":
            queryset = queryset.order_by('subject')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_list'] = MemberInfo.objects.filter(Center_Code=self.request.user.Center_Code).exclude(
            id=self.request.user.id)
        context['label_list'] = Mail.LABEL_CHOICES
        context['email_type'] = self.request.GET.get('email_type', "send")
        context['inbox_count'] = MailReceiver.objects.filter(receiver=self.request.user, mail_deleted=False,
                                                             mail_spam=False, mail_viewed=False).count()
        # context['starred_count'] = MailReceiver.objects.filter(Q(mail_starred=True, mail_deleted=False,
        #                                                          mail_spam=False, receiver=self.request.user) | Q(
        #     mail__sender_starred=True, mail__sender_delete=False,
        #     mail__sender=self.request.user)).count()
        context['starred_count'] = MailReceiver.objects.filter(receiver=self.request.user, mail_starred=True,
                                                               mail_deleted=False).count()
        context['trash_count'] = MailReceiver.objects.filter(mail_deleted=True).count()
        context['search_q'] = self.request.GET.get('search', '')
        context['filter'] = self.request.GET.get('filter', '')
        context['glc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='GR').count()
        context['slc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='SP').count()
        context['alc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='AS').count()
        context['elc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='EX').count()
        context['plc'] = MailReceiver.objects.filter(receiver=self.request.user, mail_viewed=False,
                                                     mail_deleted=False, mail_spam=False,
                                                     mail__label='PR').count()

        return context


class DraftCreateView(CreateView):
    model = Mail
    template_name = "mail/base.html"
    form_class = MailForm
    success_url = reverse_lazy('mail_send_list')

    def form_invalid(self, form):
        r = super().form_invalid(form)
        print(form.errors)
        return r

    def form_valid(self, form):
        self.success_url = self.success_url + "?email_type=draft"
        r = super().form_valid(form)
        self.object.mail_draft = True
        self.object.save()
        return r


class DraftUpdateView(UpdateView):
    model = Mail
    template_name = "mail/detail_draft.html"
    form_class = DraftUpdateForm
    success_url = reverse_lazy('mail_send_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user_list'] = MemberInfo.objects.filter(
            Center_Code=self.request.user.Center_Code
        ).exclude(id=self.request.user.id)
        context['label_list'] = Mail.LABEL_CHOICES
        context['email_type'] = self.request.GET['email_type']

        return context

    def form_invalid(self, form):
        to_return = super().form_invalid(form)
        return to_return

    def form_valid(self, form, **kwargs):
        self.success_url = self.success_url + "?email_type=draft"
        to_return = super().form_valid(form)
        self.object.mail_draft = False
        self.object.save()

        receiver_list = self.request.POST['receiver_list']
        print(receiver_list, type(receiver_list))
        r_list = []
        if len(receiver_list):
            r_list = receiver_list.split(',')

        for r in r_list:
            m_rec = MailReceiver()
            m_rec.mail = self.object
            m_rec.receiver = MemberInfo.objects.get(pk=int(r))
            m_rec.save()

        return to_return


class MailDetailView(DetailView):
    model = MailReceiver
    template_name = "mail/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['label_list'] = Mail.LABEL_CHOICES
        context['email_type'] = self.request.GET['email_type']
        return context


class SendDetailView(DetailView):
    model = Mail
    template_name = "mail/send_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['email_type'] = self.request.GET['email_type']
        return context


class MailMultipleCreate(View):
    def post(self, request, *args, **kwargs):
        m_form = MailForm(request.POST, request.FILES)
        m_obj = m_form.save(commit=False)
        m_obj.save()
        receiver_list = self.request.POST['receiver_list']

        r_list = []
        if len(receiver_list):
            r_list = receiver_list.split(',')

        print(receiver_list)
        print(r_list)

        for r in r_list:
            # required if receiver null = True, blank = True

            # mail_form = MailReceiverForm(request.POST, request.FILES)
            # mail_obj = mail_form.save(commit=False)

            # if Receiver is not blank and null then,
            mail_obj = MailReceiver()
            receiver = MemberInfo.objects.get(pk=int(r))
            mail_obj.receiver = receiver
            mail_obj.mail = m_obj
            mail_obj.save()

        # email_type = self.request.GET.get("email_type", "inbox")
        return redirect(reverse('mail_send_list') + '?email_type=send')


class ReplyCreateView(CreateView):
    model = Mail
    template_name = "mail/index.html"
    form_class = ReplyForm
    success_url = reverse_lazy('mail_list')

    def form_invalid(self, form):
        r = super().form_invalid(form)
        print(form.errors)
        return r

    def form_valid(self, form):
        self.success_url = self.success_url + "?email_type=inbox"
        r = super().form_valid(form)
        # already mentioned in form field detail.html and send_detail.html
        # self.object.reply_to = get_object_or_404(Mail, pk=self.kwargs['pk'])
        self.object.save()
        return r


def MailDeleteView(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    mail.sender_delete_p = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_send_list') + '?email_type=' + email_type)


class MailReceiverDeleteView(DeleteView):
    model = MailReceiver
    success_url = reverse_lazy('mail_list')

    def get_success_url(self):
        surl = super().get_success_url()
        print(surl, self.request.GET['email_type'])
        return surl + "?email_type=" + self.request.GET['email_type']


def mail_starred(request, pk):
    mail = get_object_or_404(MailReceiver, pk=pk)
    if mail.mail_starred:
        mail.mail_starred = False
    else:
        mail.mail_starred = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def mail_deleted(request, pk):
    mail = get_object_or_404(MailReceiver, pk=pk)
    if mail.mail_deleted:
        mail.mail_deleted = False
    else:
        mail.mail_deleted = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def mail_send(request, pk):
    mail = get_object_or_404(MailReceiver, pk=pk)
    mail.mail_send = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def mail_viewed(request, pk):
    mail = get_object_or_404(MailReceiver, pk=pk)
    mail.mail_viewed = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def mail_unread(request, pk):
    mail = get_object_or_404(MailReceiver, pk=pk)
    mail.mail_viewed = False
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def mail_spam(request, pk):
    print("spam request")
    mail = get_object_or_404(MailReceiver, pk=pk)
    mail.mail_starred = False
    if mail.mail_spam:
        mail.mail_spam = False
    else:
        mail.mail_spam = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_list') + '?email_type=' + email_type)


def sender_starred(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    if mail.sender_starred:
        mail.sender_starred = False
    else:
        mail.sender_starred = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_send_list') + '?email_type=' + email_type)


def sender_delete(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    if mail.sender_delete:
        mail.sender_delete = False
    else:
        mail.sender_delete = True
    mail.save()
    email_type = request.GET.get('email_type', "")
    return redirect(reverse('mail_send_list') + '?email_type=' + email_type)
