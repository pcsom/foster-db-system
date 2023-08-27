from concurrent.futures import process
import traceback
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from decorators import *
from accounts.models import child, userBasic
from .forms import formToReqModel, itemsRequestForm
from .models import itemsRequest
from django.conf import settings
from django.core.mail import send_mail
from utility import *
import json
import ast
from django.core.mail import get_connection, send_mail
from django.core.mail.message import EmailMessage
from mainpg.models import ReqFormSettings

# Create your views here.


@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def newRequest(request):
    if request.method == 'POST':
        form = itemsRequestForm(request.POST, parentUser=request.user)
        
        alertList = []
        redir = ""
        #print(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    newItemsRequest = formToReqModel(form)
                    newItemsRequest.forUser = request.user

                    
                    curReqs = itemsRequest.objects.filter(forUser=request.user).order_by('-date')
                    if len(curReqs) > 0:
                        newItemsRequest.preferredMethodOfReceiving = curReqs[0].preferredMethodOfReceiving
                    else:
                        newItemsRequest.preferredMethodOfReceiving = {'info': ['Pick-up at foster closet', "Mondays 8-11", "Wednesdays 8-11", "Saturdays 8-11"]}

                    newItemsRequest.save()
            except Exception as e:
                datDisp = ReqFormSettings.load().databaseDisplay
                if type(e).__name__ == "ValidationError":
                    theDict = ast.literal_eval(str(e))
                    for singleField in theDict.keys():
                        for mess in theDict[singleField]:
                            if singleField in datDisp:
                                alertList.append(f"Field '{datDisp[singleField]}' - {mess}")
                            else:
                                alertList.append(f"Field '{processName(singleField)}' - {mess}")

                elif type(e).__name__ == "ValueError":
                    mess = str(e)
                    field = mess[7:(mess[7:].find("'") + 7)]
                    if field in datDisp:
                        alertList.append(mess.replace(field, datDisp[field]))
                    else:
                        alertList.append(mess.replace(field, processName(field)))
                else: 
                    alertList.append(str(e))
            else:
                subject = 'New Request(s) Submitted'
                message = f"{request.user.userbasic.__str__()}, made a new request(s) in the NAFC Family Center."
                recipient_list = [oneAdmin.email for oneAdmin in User.objects.all() if oneAdmin.groups.exists() and oneAdmin.groups.all()[0].name == 'admin']
                
                GMAIL_SERVICE = initGmailAPI()
                send_message(GMAIL_SERVICE, 'me', create_message("me", ", ".join(recipient_list), subject, message))
                
                messages.success(request, "Your request has been submitted. You will recieve an email alert once the items have been collected.")

                if request.POST['submitter'] == '0':
                    redir = 'new-request'
                else:
                    redir = 'receiving'
        else:
            for singleField in form.errors.keys():
                for singleMess in form.errors[singleField]:
                    alertList.append(f"{singleField} - {singleMess}")
        return JsonResponse([alertList, redir], safe=False)    
    else:
        children = child.objects.filter(parent=request.user).all()
        numChild = len(children)
        basicInfo = request.user.userbasic
        form = itemsRequestForm(parentUser=request.user)
        context = {
            'children': children, 'basicInfo': basicInfo, 'form': form, 'curUser': request.user, 'numChild': numChild
        }
        return render(request, "irequests/newRequest.html", context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def receiving(request):
    if request.method == 'POST':
        vals = []
        if request.POST['method'] == "special":
            vals.append("Special arrangement")
        elif request.POST['method'] == "pickup":
            vals.append("Pick-up at foster closet")
            if "mon" in request.POST:
                vals.append("Mondays 8-11")
            if "tue" in request.POST:
                vals.append("Tuesdays 8-11")
            if "wed" in request.POST:
                vals.append("Wednesdays 8-11")
            if "thu" in request.POST:
                vals.append("Thursdays 8-11")
            if "fri" in request.POST:
                vals.append("Fridays 8-11")
            if "sat" in request.POST:
                vals.append("Saturdays 8-11")

            if len(vals) == 1:
                return JsonResponse([False, "Please select at least one pick-up option."], safe=False)

        for oneReq in itemsRequest.objects.filter(forUser=request.user).all():
            if oneReq.status == "Pending" or oneReq.status == "Collecting":
                oneReq.preferredMethodOfReceiving = {'info': vals}
                oneReq.save()

        messages.success(request, "Your preferred method of receiving has been set.")
        return JsonResponse([True, "/"], safe=False)

    else:
        reqs = itemsRequest.objects.filter(forUser=request.user).order_by('-date')
        pmor = {}
        special, pickup, noReqs = False, False, False
        try:
            pmor = reqs[0].preferredMethodOfReceiving
            if pmor['info'][0] == "Pick-up at foster closet":           #MUST BE CHANGED IF THE VALUE STORED IN DB CHANGES
                pickup = True
            elif pmor['info'][0] == "Special arrangement":
                special = True
        except:
            noReqs = True

        context = {'special': json.dumps(special), 'pickup': json.dumps(pickup), 'selfId': request.user.id, 'noReqs': noReqs}
        try:
            context['rest'] = json.dumps([x[0:3].lower() for x in pmor['info'][1:]])
        except:
            context['rest'] = json.dumps([])

        return render(request, 'irequests/receiving.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
@modified_access
def viewRequests(request, pk):
    authList = adminAuth(request, pk)
    if request.method == "POST":
        dbId = request.POST['dbId']
        curReq = itemsRequest.objects.get(forUser=request.user, id=dbId)
        if authList['toManage'] == curReq.forUser:
            return JsonResponse(curReq.get_fields(strDate=True), safe=False)
    else:
        itemsRequestsRaw = itemsRequest.objects.filter(forUser=authList['toManage']).all()
        iRequests = []
        ctr = 0
        for one in itemsRequestsRaw[::-1]:
            iRequests.append({'id': ctr, 'dbId': one.id, 'childDateInfo': one.childDateInfo()})
            ctr += 1
        
        context = {'itemsRequests': json.dumps(iRequests), 'rev': iRequests, 'pn': authList['pn'], 'plainPn': authList['plainPn'], 'numReq': len(iRequests), 'pk':pk, 'verb':'have' if authList['plainPn']=="you" else 'has'}
        return render(request, 'irequests/viewRequests.html', context)

    