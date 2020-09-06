from django.forms import ModelForm

from mail.models import Mail, MailReceiver


class DraftUpdateForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"


class MailReceiverForm(ModelForm):
    class Meta:
        model = MailReceiver
        fields = "__all__"


class MailForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"


class ReplyForm(ModelForm):
    class Meta:
        model = Mail
        fields = "__all__"
        exclude = ['label']