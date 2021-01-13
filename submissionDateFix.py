# For running this script use "python3 manage.py shell < submissionDateFix.py"

from WebApp.models import AssignAnswerInfo

def submissionDateFix():
    all_answers=AssignAnswerInfo.objects.all()
    for answer in all_answers:
        answer.Submission_Date = answer.Register_DateTime
        answer.save()

submissionDateFix()