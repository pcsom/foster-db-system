from urllib.request import Request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth, Group
from django.contrib.auth.decorators import login_required
from decorators import unauthenticated_user, allowed_users, modified_access
from .models import userBasic, careType, child, adoptiveFamily, fosterFamily, kinshipFamily, safetyFamily
from django.http import HttpResponse
from django.forms.models import model_to_dict
from .forms import *
from utility import *
from django.db import transaction
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
import ast
from adminManagement.models import volunteer
from django.contrib.auth import update_session_auth_hash, password_validation
from datetime import datetime
import traceback
import datetime
# Create your views here.


@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if(user.userbasic.registrationProgress == 'Complete'):
                return redirect('/')
            else:  
                messages.error(request, 'Please complete the steps on this page to continue.')
                return redirect(f'type-of-care/{user.id}')
        else:
            messages.error(request, 'Sorry, the username and password do not match!')
            return redirect('login')

    else:
        return render(request, 'login.html')



@unauthenticated_user
def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_ = request.POST['email']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        alertList = []
        pw = False

        if password1!=password2:
            alertList.append('Password confirmation failed! Please re-enter the password fields.')
        elif User.objects.filter(username=username).exists():
            alertList.append('There is an account already registered with this username! Please enter a different username.')
        elif User.objects.filter(email=email_).exists():
            alertList.append('There is an account already registered with this email! Please enter a different email.')
        else:
            uform = userBasicForm(request.POST)
            if uform.is_valid():
                try:
                    password_validation.validate_password(password1, request.user)
                    pw = True
                    with transaction.atomic():          #USE TRANSITION.ATOMIC() FOR ANY SAVE OR CREATE OPERATION ON THE DATABASE - IT REVERTS ALL EDITS IF ANY ERROR IS DETECTED
                        newUserBasic = uform.save()
                        newUser = User.objects.create_user(username=username, password=password1, email=email_, first_name=first_name, last_name=last_name)
                        newUser.groups.add(Group.objects.get(name='user'))
                        newUser.save()

                        newUserBasic.user = newUser
                        newUserBasic.registrationProgress='type-of-care'
                        newUserBasic.save()
                except Exception as e:
                    if type(e).__name__ == "ValidationError":
                        theDict = ast.literal_eval(str(e))
                        if pw:
                            for singleField in theDict.keys():
                                for mess in theDict[singleField]:
                                    alertList.append(f"Field '{singleField}' - {mess}")
                        else:
                            alertList.extend([mess for mess in theDict])
                    elif type(e).__name__ == "ValueError":
                        mess = str(e)
                        field = mess[7:(mess[7:].find("'") + 7)]
                        alertList.append(mess.replace(field, processName(field)))
                    else: 
                        alertList.append(str(e))

                else:
                    messages.success(request, "Account successfully created! Please Log In to continue.")
            else:
                for singleField in uform.errors.keys():
                    for singleMess in uform.errors[singleField]:
                        alertList.append(f"{singleField} - {singleMess}")
        return JsonResponse(alertList, safe=False)
    else:
        form = userBasicForm()
        context = {'form': form}
        return render(request, 'register.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def changeUsername(request, pk):
    authList = adminAuth(request, pk)

    if authList['goHome']:
        return redirect('/')
    toManage = authList['toManage']

    if request.method =="POST":
        newUsername = request.POST['updateUsername']
        if uniqueUsername(toManage, newUsername):
            #User.objects.filter(email=toManage.email).update(username=newUsername)
            toManage.username = newUsername
            toManage.save()
            messages.success(request, "Successfully changed username!")
            subject = 'NAFC Username Changed'
            message = f"Hello {toManage.first_name} {toManage.last_name},\n\nYour North Alabama Foster Closet username was changed. Your new username is '{toManage.username}'\nPlease remember to use this new username when logging into the NAFC website. Thank you!\n\nNAFC Team"
            recipient_list = [str(toManage.email),]
            
            GMAIL_SERVICE = initGmailAPI()
            sent = send_message(GMAIL_SERVICE, 'me', create_message("me", ", ".join(recipient_list), subject, message))
            if not sent and not adminAuth['same']:
                messages.error(request, "Was not able to notify this user about their new username via email. Please ensure the email system is working.")
            return redirect(authList['redir'])
        else:
            messages.error(request, 'Someone else already registered an account with the username you provided!')
            context = {'username': newUsername, 'pn': authList['pn']}
            return render(request, "changeUsername.html", context)
    else:
        context = {'username': toManage.username, 'pn': authList['pn']}
        return render(request, "changeUsername.html", context)




#Intentionally excluded the @allowed_users decorator since it won't pass if progress != complete
@login_required(login_url='login')
def typeOfCare(request, pk):
    authList = adminAuth(request, pk)
    if authList['pn'] == 'your':
        authList['pn'] = "Your"
    toManage = authList['toManage']
    alertList = []
    newUser = toManage.userbasic.registrationProgress == 'type-of-care'
    noCt = True
    curCare = careType.objects.filter(user=toManage).first()
    if curCare:
        noCt = False

    if request.method == 'POST':
        adoptive, foster, kinship, safety = False, False, False, False
        if "careType1" in request.POST:
            adoptive = True
        if "careType2" in request.POST:
            foster = True
        if "careType3" in request.POST:
            kinship = True
        if "careType4" in request.POST:
            safety = True


        try:
            signature = None
            if (newUser or noCt) and authList['same']:
                signature = request.POST['signature']
                date = request.POST['date']
                if not signature:
                    raise ValidationError({'signature': 'This is required'})
                if not date:
                    raise ValidationError({'date': 'This is required'})
                if not checkDate(date):
                    raise ValidationError({'date': 'Date format must be MM/DD/YYYY'})

            with transaction.atomic():
                caredef={'adoptive': adoptive, 'foster': foster, 'kinship': kinship, 'safety': safety, 'name': str(toManage)}
                if (newUser or noCt) and authList['same']:
                    caredef['signature'] = signature
                    caredef['date'] = datetime.datetime.strptime(date, '%m/%d/%Y').date()
                careType.objects.update_or_create(
                    user=toManage,
                    defaults=caredef
                )


                    
                if(adoptive):
                    adoptiveFamily.objects.update_or_create(
                        user=toManage,
                    )
                elif(adoptiveFamily.objects.filter(user=toManage).exists()):
                    adoptiveFamily.objects.filter(user=toManage).delete()
                


                if(foster):
                    fosterFamily.objects.update_or_create(
                        user=toManage,
                        defaults={'county': request.POST['fosterCounty'], 'agency': request.POST['agency'],
                        'workerName': request.POST['fosterSocialWorkerName'], 'workerContact': request.POST['fosterSocialWorkerContact']}
                    )
                elif(fosterFamily.objects.filter(user=toManage).exists()):
                    fosterFamily.objects.filter(user=toManage).delete()
                

                if(kinship):
                    kinshipFamily.objects.update_or_create(
                        user=toManage,
                        defaults={'children': request.POST['kinshipChildren'], 'placementRelation': request.POST['placementRelation'],
                        'county': request.POST['kinshipCounty'], 'workerName': request.POST['kinshipSocialWorkerName'],
                        'workerContact': request.POST['kinshipSocialWorkerContact']}
                    )
                elif(kinshipFamily.objects.filter(user=toManage).exists()):
                    kinshipFamily.objects.filter(user=toManage).delete()


                if(safety):
                    safetyFamily.objects.filter(user=toManage).update_or_create(
                        user=toManage,
                        defaults={'county': request.POST['safetyCounty'], 'planTimeLength': request.POST['planTimeLength'],
                        'workerName': request.POST['safetySocialWorkerName'], 'workerContact': request.POST['safetySocialWorkerContact']}
                    )
                elif(safetyFamily.objects.filter(user=toManage).exists()):
                    safetyFamily.objects.filter(user=toManage).delete()

                if newUser and authList['same']:
                    #userBasic.objects.filter(user=toManage).update(registrationProgress='Complete')
                    toManage.userbasic.registrationProgress = 'Complete'
                    toManage.userbasic.save()
        except Exception as e:
            traceback.print_exc()
            if type(e).__name__ == "ValidationError":
                theDict = ast.literal_eval(str(e))
                for singleField in theDict.keys():
                    for mess in theDict[singleField]:
                        alertList.append(f"Field '{singleField}' - {mess}")
            elif type(e).__name__ == "ValueError":
                mess = str(e)
                field = mess[7:(mess[7:].find("'") + 7)]
                alertList.append(mess.replace(field, processName(field)))
            else: 
                alertList.append(str(e))

            return JsonResponse([alertList, ''], safe=False)
        else:
            if newUser and authList['same']:
                messages.success(request, "Your information has been saved! Welcome to NAFC's family center! Please use the form below to add your child(ren)'s information to your account, one at a time; if you want to do this at a later time, click on 'Dashboard' above to go to the dashboard.")
                return JsonResponse([alertList, f'/add-child/{toManage.id}'], safe=False)
            else:
                messages.success(request, f"{authList['pn']} care type information has been saved!")
                return JsonResponse([alertList, authList['redir']], safe=False)

    else:
        context = {'pk': pk, 'unsigned': False, 'same':authList['same'], 'pn': authList['pn']}
        if (newUser or noCt):
            context['unsigned'] = True
        if careType.objects.filter(user=toManage).exists():
            context.update({
                'careType': careType.objects.filter(user=toManage).first(),
                'adoptive': adoptiveFamily.objects.filter(user=toManage).first(),
                'foster': fosterFamily.objects.filter(user=toManage).first(),
                'kinship': kinshipFamily.objects.filter(user=toManage).first(),
                'safety': safetyFamily.objects.filter(user=toManage).first(),
            })
        return render(request, 'typeOfCare.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
@modified_access
def addChild(request, pk):
    authList = adminAuth(request, pk)
    uId = authList['toManage'].id
    pn = authList['pn']
    
    if request.method == 'POST':
        alertList = []

        uform = childForm(request.POST)
        if uform.is_valid() and ('hasAllergy' not in request.POST or 'hasAllergy' in request.POST and request.POST['allergyDescription'] != ''):
            try:
                with transaction.atomic():
                    newChild = uform.save()
                    newChild.parent = authList['toManage']
                    newChild.save()
            except Exception as e:
                if type(e).__name__ == "ValidationError":
                    theDict = ast.literal_eval(str(e))
                    for singleField in theDict.keys():
                        for mess in theDict[singleField]:
                            alertList.append(f"Field '{singleField}' - {mess}")
                elif type(e).__name__ == "ValueError":
                    mess = str(e)
                    field = mess[7:(mess[7:].find("'") + 7)]
                    alertList.append(mess.replace(field, processName(field)))
                else: 
                    alertList.append(str(e))
                return JsonResponse([alertList, ''], safe=False)
            else:
                messages.success(request, f"A child has been successfully added to {pn} account!")
                if request.POST['submitter'] == "Save and Add Another Child":
                    return JsonResponse([alertList, f'/add-child/{pk}'], safe=False)
                else:
                    return JsonResponse([alertList, authList['redir']], safe=False)
        else:
            for singleField in uform.errors.keys():
                for singleMess in uform.errors[singleField]:
                    alertList.append(f"{singleField} - {singleMess}")
            if 'hasAllergy' in request.POST and request.POST['allergyDescription'] == '':
                alertList.append("Please describe allergies.")
            return JsonResponse([alertList, ''], safe=False)
    else:
        form = childForm()
        #EDIT FORM LABEL FOR NEW TO YOUR HOME (PLACEMENT) TO USE PN NOT YOUR
        context = {'form': form, 'saving': 'add', 'back': authList['redir'], 'pk': pk, 'action': 'add', 'pn':pn}
        return render(request, 'children/children.html', context)



#intentionally excluded modified_access decorator
@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def updateChild(request, pk):
    currentChild = child.objects.get(id=pk)
    authList = adminAuth(request, currentChild.parent.id)


    uform = childForm(instance=currentChild)


    if request.method == 'POST':
        uform = childForm(request.POST, instance=currentChild)
        alertList = []
        if uform.is_valid() and ('hasAllergy' not in request.POST or 'hasAllergy' in request.POST and request.POST['allergyDescription'] != ''):
            try:
                with transaction.atomic():
                    uform.save()
            except Exception as e:
                if type(e).__name__ == "ValidationError":
                    theDict = ast.literal_eval(str(e))
                    for singleField in theDict.keys():
                        for mess in theDict[singleField]:
                            alertList.append(f"Field '{singleField}' - {mess}")
                elif type(e).__name__ == "ValueError":
                    mess = str(e)
                    field = mess[7:(mess[7:].find("'") + 7)]
                    alertList.append(mess.replace(field, processName(field)))
                else: 
                    alertList.append(str(e))
                return JsonResponse([alertList, ''], safe=False)
            else:
                messages.success(request, "Successfully updated child's information.")
                return JsonResponse([alertList, authList['redir']], safe=False)
        else:
            for singleField in uform.errors.keys():
                for singleMess in uform.errors[singleField]:
                    alertList.append(f"{singleField} - {singleMess}")
            if 'hasAllergy' in request.POST and request.POST['allergyDescription'] == '':
                alertList.append("Please describe allergies.")
            return JsonResponse([alertList, ''], safe=False)
    else:
        uform.fields['newPlacement'].label = f"Is this child new to {authList['pn']} home (new placement)? : *"
        uform.fields['relationship'].label = f"{authList['pn'].capitalize()} relationship to this child: *"
        context = {'form': uform, 'saving': 'update', 'pn': authList['pn'], 'back': authList['redir'], 'pk': pk, 'action': 'update'}
        return render(request, 'children/children.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def deleteChild(request, pk):
    currentChild = child.objects.get(id=pk)
    authList = adminAuth(request, currentChild.parent.id)

    if currentChild not in child.objects.filter(parent = request.user) and not authList['group'] == 'admin':
        return render(request, 'notAuth.html')

    if request.method == "POST":
        currentChild.delete()
        messages.success(request, "Child has been deleted.")
        return redirect(authList['redir'])
    
    context = {'child': currentChild, 'redir': authList['redir']}
    return render(request, 'children/deleteChild.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['user', 'admin'])
def updateBasic(request, pk):
    authList = adminAuth(request, pk)
    if authList['goHome']:
        return redirect('/')

    uform = userBasicForm(instance=authList['toManage'].userbasic)

    if request.method == 'POST':
        uform = userBasicForm(request.POST, instance=authList['toManage'].userbasic)
        alertList = []
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email_ = request.POST['email']

        if not uniqueEmail(authList['toManage'], email_):
            alertList.append('Someone else already registered an account with the email you provided!')
        elif uform.is_valid():
            try:
                with transaction.atomic():
                    uform.save()
                    User.objects.filter(username=authList['toManage'].username).update(email=email_, first_name=first_name, last_name=last_name)
            except Exception as e:
                if type(e).__name__ == "ValidationError":
                    theDict = ast.literal_eval(str(e))
                    for singleField in theDict.keys():
                        for mess in theDict[singleField]:
                            alertList.append(f"Field '{singleField}' - {mess}")
                elif type(e).__name__ == "ValueError":
                    mess = str(e)
                    field = mess[7:(mess[7:].find("'") + 7)]
                    alertList.append(mess.replace(field, processName(field)))
                else: 
                    alertList.append(str(e))
            else:
                messages.success(request, "User information has been updated.")
        else:
            for singleField in uform.errors.keys():
                for singleMess in uform.errors[singleField]:
                    alertList.append(f"{singleField} - {singleMess}")
        return JsonResponse([alertList, authList['redir']], safe=False)

    else:
        context = {**{'back':authList['redir'], 'pk': pk, 'form': uform, 'curUser': authList['toManage'], 'pn':authList['pn'][0].upper() + authList['pn'][1:]}, **model_to_dict(userBasic.objects.get(user=authList['toManage']))}
        return render(request, 'updateBasic.html', context)




@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')




def passwordChange(request):
    if request.method == "POST":
        alertList = []
        passrep, newpass, passconf = request.POST['oldpass'], request.POST['newpass'], request.POST['newpassconf']
        if not request.user.check_password(passrep):
            alertList.append("Old password is incorrect. If you forgot it, use the \"reset it through email\" button above.")
            return JsonResponse([False, alertList], safe=False)
        elif newpass != passconf:
            alertList.append("The new password and confirmation do not match; please re-enter them.")
        else:
            try:
                password_validation.validate_password(newpass, request.user)
                with transaction.atomic():
                    request.user.set_password(newpass)
                    request.user.save()
                    update_session_auth_hash(request, request.user)         #Pw change breaks user's session; call this to re-assign session, so that confirmation message will carry over uninterrupted
            except Exception as e:
                if type(e).__name__ == "ValidationError":
                    theDict = ast.literal_eval(str(e))
                    alertList.extend([mess for mess in theDict])
                else:
                    alertList.append(str(e))
                return JsonResponse([False, alertList], safe=False)
            messages.success(request, "Password has been successfully changed.")
            return JsonResponse([True, "/"], safe=False)
        return JsonResponse([False, alertList], safe=False)
    else:
        return render(request, 'passwordChange.html')
