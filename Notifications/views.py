# Create your views here.
from django.contrib.auth.decorators import login_required
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import ListView

from Notifications.models import Notification


class NotificationViewList(ListView):
    template_name = 'Notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 1

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(NotificationViewList, self).dispatch(
            request, *args, **kwargs)


class AllNotificationsList(NotificationViewList):
    """
    Index page for authenticated user
    """

    def get_queryset(self):
        qset = self.request.user.notifications.all()
        return qset


class SeeAllNotificationsList(NotificationViewList):
    """
    Index page for authenticated user
    """
    template_name = "Notifications/all_notifications.html"

    def get_queryset(self):
        qset = self.request.user.notifications.all()
        return qset

class UnreadNotificationsList(NotificationViewList):
    def get_queryset(self):
        return self.request.user.notifications.unread()


@login_required
def mark_all_as_read(request):
    request.user.notifications.mark_all_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    if request.is_ajax():
        return JsonResponse({'message': 'success'}, status=200)

    return redirect('Notifications:unread')


@login_required
def mark_as_read(request, pk=None):
    notification_id = pk

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_read()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    if request.is_ajax():
        return JsonResponse({'message': 'success'}, status=200)

    return redirect('Notifications:all')


@login_required
def mark_as_unread(request, pk):
    notification_id = pk

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.mark_as_unread()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    if request.is_ajax():
        return JsonResponse({'message': 'success'}, status=200)

    return redirect('Notifications:all')


@login_required
def delete(request, pk):
    notification_id = pk

    notification = get_object_or_404(
        Notification, recipient=request.user, id=notification_id)
    notification.delete()

    _next = request.GET.get('next')

    if _next:
        return redirect(_next)

    if request.is_ajax():
        return JsonResponse({'message': 'success'}, status=200)

    return redirect('Notifications:all')


@never_cache
def live_unread_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0
        }
    else:
        data = {
            'unread_count': request.user.notifications.unread().count(),
        }
    return JsonResponse(data)


@never_cache
def live_unread_notification_list(request):
    ''' Return a json with a unread notification list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'unread_count': 0,
            'unread_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = 10
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    unread_list = []

    for notification in request.user.notifications.unread()[0:num_to_fetch]:
        struct = model_to_dict(notification)
        if notification.creator:
            struct['actor'] = str(notification.creator)
        if notification.target:
            struct['target'] = str(notification.target)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)

        unread_list.append(struct)
        if request.GET.get('mark_as_read'):
            notification.mark_as_read()
    data = {
        'unread_count': request.user.notifications.unread().count(),
        'unread_list': unread_list
    }
    return JsonResponse(data)


@never_cache
def live_all_notification_list(request):
    ''' Return a json with a unread notification list '''
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0,
            'all_list': []
        }
        return JsonResponse(data)

    default_num_to_fetch = 10
    try:
        # If they don't specify, make it 5.
        num_to_fetch = request.GET.get('max', default_num_to_fetch)
        num_to_fetch = int(num_to_fetch)
        if not (1 <= num_to_fetch <= 100):
            num_to_fetch = default_num_to_fetch
    except ValueError:  # If casting to an int fails.
        num_to_fetch = default_num_to_fetch

    all_list = []

    for notification in request.user.notifications.all()[0:num_to_fetch]:
        struct = model_to_dict(notification)
        if notification.creator:
            struct['actor'] = str(notification.creator)
        if notification.target:
            struct['target'] = str(notification.target)
        if notification.action_object:
            struct['action_object'] = str(notification.action_object)

        all_list.append(struct)
        if request.GET.get('mark_as_read'):
            notification.mark_as_read()
    data = {
        'all_count': request.user.notifications.count(),
        'unread_count': request.user.notifications.filter(unread=True).count(),
        'all_list': all_list
    }
    return JsonResponse(data, json_dumps_params={'indent': 4})


def live_all_notification_count(request):
    try:
        user_is_authenticated = request.user.is_authenticated()
    except TypeError:  # Django >= 1.11
        user_is_authenticated = request.user.is_authenticated

    if not user_is_authenticated:
        data = {
            'all_count': 0
        }
    else:
        data = {
            'all_count': request.user.notifications.count(),
        }
    return JsonResponse(data)
