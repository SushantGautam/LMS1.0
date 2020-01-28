from django.contrib import messages
from django.shortcuts import redirect


class AdminAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, admn=1) == 1 else redirect('login')


class TeacherAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, tchr=1) == 1 else redirect('login')


class StudentAuthMxnCls:
    def get(self, request, *args, **kwargs):
        # Checks if AuthCheck passed test for admin by returning 1 else exits
        return super().get(request, *args, **kwargs) if AuthCheck(request, stdn=1) == 1 else redirect('login')


def AuthCheck(request, admn=0, tchr=0, stdn=0):
    initStat = 1
    try:
        if admn:
            if not request.user.Is_CenterAdmin:
                initStat *= 0
        if tchr:
            if not request.user.Is_Teacher:
                initStat *= 0

        if stdn:
            if not request.user.Is_Studnet:
                initStat *= 0
    except:
        return redirect('login')

    if initStat:
        return 1
    else:
        messages.error(request,
                       'The path you entered into the system was not suitable for your role and you were redirected.')
        return redirect('login')
