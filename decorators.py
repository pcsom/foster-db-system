from django.http import HttpResponse
from django.shortcuts import redirect, render
from utility import adminAuth
from django.contrib import messages
from mainpg.models import ServiceAccountInfo
import logging
log = logging.getLogger(__name__)


"""def NAME_OF_DECORATOR(view_func):
    def wrapper_func(request, *args, **kwargs):

        return view_func(request, *args, **kwargs)

    return wrapper_func"""



def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func



def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            serv = ServiceAccountInfo.load()
            log.debug(f"{serv.serviceActive}")
            if not serv.serviceActive:
                log.debug("NOT ACTIVE")
                messages.error(request, "Email service account is out of order. Please alert an NAFC volunteer or worker.")
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                if(request.user.userbasic.registrationProgress == 'Complete'):
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, "Please complete the steps on this page to continue.")
                    return redirect(f"{request.user.userbasic.registrationProgress}/{request.user.id}")
            else:
                return render(request, 'notAuth.html')
        return wrapper_func
    return decorator



def modified_access(view_func):
    def wrapper_func(request, *args, **kwargs):
        authList = adminAuth(request, int(kwargs['pk']))
        if authList['goHome']:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func
