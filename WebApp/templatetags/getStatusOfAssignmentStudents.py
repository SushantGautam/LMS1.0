from django import template

register = template.Library()


@register.simple_tag
def getStatusoOfAssignment(obj, user):
    status = obj.get_student_assignment_status(user)
    if status:
        return 'Complete'
    else:
        return 'Incomplete'
    return status
