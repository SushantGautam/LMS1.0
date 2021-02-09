from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.decorators.http import require_POST

from Notifications.models import Notification
from comment.models import Comment, Reaction, ReactionInstance, ContentType


@method_decorator(require_POST, name='dispatch')
class SetReaction(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        created = False

        if not request.is_ajax():
            return HttpResponseBadRequest(_('Only AJAX request are allowed'))

        reaction_type = kwargs.get('reaction', None)
        reaction_obj = Reaction.objects.get_reaction_object(comment)
        try:
            created = ReactionInstance.objects.set_reaction(user=request.user, reaction=reaction_obj,
                                                            reaction_type=reaction_type)
        except ValidationError as e:
            return HttpResponseBadRequest(e.messages)

        comment.reaction.refresh_from_db()
        response = {
            'status': 0,
            'likes': comment.likes,
            'dislikes': comment.dislikes,
            'msg': _('Your reaction has been updated successfully')
        }

        notific = Notification.objects.filter(action_object_object_id=comment.content_object.id,
                                              action_object_content_type=ContentType.objects.get_for_model(
                                                  comment.content_object).id,
                                              recipient=comment.user,
                                              verb__icontains='liked your comment')
        # ReactionInstance.objects.send_notification(notific=notific, comment=comment, user=request.user, created=created)

        if created:
            if request.user.pk != comment.user.pk:
                if notific.exists():
                    verb = None
                    if comment.likes > 1:
                        verb = 'and {} others liked your comment'.format(int(comment.likes) - 1)
                        description = '{} and {} others liked your comment'.format(request.user.username,
                                                                                   int(comment.likes) - 1)
                    else:
                        verb = 'liked your comment'
                        description = '{} liked your comment'.format(request.user.username)
                    notific.update(
                        creator=request.user,
                        verb=verb,
                        description=description
                    )
                else:
                    from Notifications.signals import notify
                    notify.send(
                        sender=request.user,
                        recipient=comment.user,
                        verb='liked your comment',
                        description='{} liked your comment.'.format(request.user.username),
                        action_object=comment.content_object,
                    )
        else:
            if comment.likes == 0:
                notific.delete()
            else:
                if comment.likes > 1:
                    description = '{} and {} others liked your comment'.format(
                        comment.reaction.get_reactors(reaction_type=1).first().user,
                        int(comment.likes) - 1)
                else:
                    description = '{} liked your comment'.format(
                        comment.reaction.get_reactors(reaction_type=1).first().user)
                notific.update(
                    description=description
                )

        return JsonResponse(response)
