# This file contains template tags for template-model relation.

from django import template

register = template.Library()


# For finding the submission status of surveys
@register.simple_tag
def getSurveyStatus(obj, user):
    can_submit, datetimeexpired, options, questions = obj.can_submit(user)
    return can_submit, datetimeexpired, options, questions

# @register.simple_tag
# def canTakeQuiz(obj, user):
#     sitting = obj.can_take(user)
#     return sitting
