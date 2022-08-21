from django.contrib.auth.models import User, auth, Group
from itertools import chain
from datetime import datetime

from django.db.models import fields
from django.db.models.fields import *
import re

from django.core.exceptions import ValidationError
#from django.utils.translation import ugettext as _
from django.utils.translation import gettext as _, ngettext

import os

from google.auth.transport.requests import Request
from google.auth.exceptions import TransportError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
import json
from mainpg.models import *

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']



def pVal(pw, alertList):
    beflen = len(alertList)
    if len(pw) < 8:
        alertList.append("Password must be at least 8 characters long.")
    lowe, uppe = False, False
    for i in pw:
        if i >= 'a' and i <= 'z':
            lowe = True
        if i >= 'A' and i <= 'Z':
            uppe = True
    
    if pw.isalpha():
        alertList.append("Password must have at least one number")
    if pw.isalnum():
        alertList.append("Password must have at least one special character, such as one of the following: * $ @ # % / > &")
    if not lowe:
        alertList.append("Password must have at least one lowercase letter")
    if not uppe:
        alertList.append("Password must have at least one uppercase letter")

    return len(alertList) - beflen == 0


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall('\d', password):
            raise ValidationError(
                _("The password must contain at least 1 digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 digit, 0-9."
        )


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least 1 uppercase letter, A-Z."),
                code='password_no_upper',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 uppercase letter, A-Z."
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least 1 lowercase letter, a-z."),
                code='password_no_lower',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least 1 lowercase letter, a-z."
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                _("The password must contain at least one symbol, such as one of the following: * $ @ # % / > &"),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one symbol, such as one of the following: * $ @ # % / > &"
        )
        


def checkDate(date):
    try:
        datetime.strptime(date, '%m/%d/%Y')
        return True
    except ValueError:
        return False



def processName(fieldName):     #Formalize a variable/field name to present to user. Ex. shortSleeveShirts -> Short Sleeve Shirts
    rawStr = ""
    for letter in fieldName:
        if ord(letter) in range(ord('A'), ord('Z') + 1) and rawStr != "" and rawStr[-1] != ' ':
            rawStr = rawStr + f" {letter}"
        else:
            rawStr = rawStr + letter

    if ord(rawStr[0]) in range(ord('a'), ord('z') + 1):
        return f"{chr(ord(rawStr[0]) - ord('a') + ord('A'))}{rawStr[1:]}"
    else:
        return rawStr
    


def deProcessName(fieldName):   #Reverse of processName()
    return fieldName[0].lower() + fieldName[1:].replace(" ", "")



def uniqueEmail(user, email_):
    for one in User.objects.filter(email=email_):
        if not one == user:
            return False
    return True



def uniqueUsername(user, name):
    for one in User.objects.filter(username=name):
        if not one == user:
            return False
    return True



def adminAuth(request, pk):
    toManage = User.objects.get(id=pk)
    same = toManage == request.user

    group = None
    if request.user.groups.exists():
        group = request.user.groups.all()[0].name

    pn = "your"     #Pronoun/proper noun to display when a webpage is rendered
    plainPn = "you"
    if not same:
        pn = f"{str(toManage)}'s"
        plainPn = toManage.first_name + ' ' + toManage.last_name

    goHome = group == 'user' and not same

    redir = "/"
    if not same:
        redir = f"/view-family/{toManage.id}"

    return {'toManage': toManage, 'group': group, 'pn': pn, 'goHome': goHome, 'redir': redir, 'plainPn': plainPn, 'same':same}


def getFieldsOfType(instance, fieldType, id=False):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        val = f.value_from_object(instance)
        if f.get_internal_type() in f"{fieldType}":
            data[f.name] = val

    if not id and 'id' in data:
        del data['id']

    return data
    


def getKeys(instance, exclude=set(), overrideName={}, keepDataTableInfo=False):
    fieldsList = []
    if not keepDataTableInfo:
        exclude.add('dataTableInfo')
    for field in instance._meta.get_fields():
        curName = field.name
        if curName in exclude:
            exclude.remove(curName)
        else:
            toAdd = field.name
            if toAdd in overrideName:
                toAdd = overrideName[toAdd]
            fieldsList.append(toAdd)
    return fieldsList


def to_dict(instance, exclude=[], formatDate=[], display=[], objField={}, applyFunc={}, formatBool=[], keepDataTableInfo=False):      #Both are neck-and-neck in terms of time taken. Which better? How improve?
    # fieldsList = []
    # for field in instance._meta.get_fields():
    #     curName = field.name
    #     val = eval(f"instance.{curName}")
    #     if curName in display:
    #         display.remove(curName)
    #         fieldsList.append(eval(f"instance.get_{curName}_display()"))
    #     else:
    #         if formatDate and isinstance(val, datetime.date):
    #             fieldsList.append(f"{val.month:02}/{val.day:02}/{val.year:04}")
    #         else:
    #             if curName in objField:
    #                 fieldsList.append(eval(f"instance.{curName}.{objField[curName]}"))
    #                 del objField[curName]
    #             else:
    #                 fieldsList.append(val)
    # for i in exclude:
    #     fieldsList.remove(eval(f"instance.{i}"))
    # return fieldsList[1:]

    #CHECK SPEED AGAIN
    def singleInfo(aField):
        return (aField.name, getattr(instance, aField.name))
    fieldsList = dict(map(singleInfo, chain(instance._meta.concrete_fields, instance._meta.private_fields)))
    
    # print([aField if aField.name is not None and aField.name not in exclude else exclude.remove(aField.name) for aField in instance._meta.get_fields()])
    # fieldsList = [(aField.name, getattr(instance, aField.name)) if aField.name is not None and aField.name not in exclude else exclude.remove(aField.name) for aField in instance._meta.get_fields()]

    if 'dataTableInfo' in fieldsList and not keepDataTableInfo:
        del fieldsList['dataTableInfo']
    for i in exclude:
        del fieldsList[i]
    for i in formatDate:
        val = getattr(instance, i)
        fieldsList[i] = f"{val.month:02}/{val.day:02}/{val.year:04}"
    for i in display:
        fieldsList[i] = getattr(instance, f"get_{i}_display")()
    for i in applyFunc:
        fieldsList[i] = eval(f"{applyFunc[i]}({fieldsList[i]})")
    for i in objField:
        if objField[i][-2:] == "()":
            fieldsList[i] = getattr(getattr(instance, i), objField[i][:-2])()
        else:
            fieldsList[i] = getattr(getattr(instance, i), objField[i])
    for i in formatBool:
        if fieldsList[i] == True:
            fieldsList[i] = "Yes"
        else:
            fieldsList[i] = "No"

    return fieldsList


def getVals(instance, exclude=[], formatDate=[], display=[], objField={}, applyFunc={}, formatBool=[], keepDataTableInfo=False):
    return list(to_dict(instance, exclude, formatDate, display, objField, applyFunc, formatBool, keepDataTableInfo).values())



# def to_dict(instance, exclude=[], formatDate=False, display=[], objField=[]):
#     opts = instance._meta
#     data = {}
#     for f in chain(opts.concrete_fields, opts.private_fields):
#         if f.name in exclude:
#             continue
#         data[f.name] = f.value_from_object(instance)
#         if f.name in display:
#             exec(f"data[f.name] = instance.get_{f.name}_display()")

#         if formatDate and isinstance(data[f.name], datetime.date):
#             data[f.name] = f"{data[f.name].month:02}/{data[f.name].day:02}/{data[f.name].year}"


#     for i in exclude:
#         del data[i]
#     for one in objField:
#         data[one[0]] = eval(f"instance.{one[0]}.{one[1]}")
#     for i in objField:
#         if objField[i][-2:] == "()":
#             data[i] = getattr(getattr(instance, i), objField[i][:-2])()
#         else:
#             data[i] = getattr(instance, f"{i}.{objField[i]}")


#     return data


def binarySearch(arr, x, modifier=""):
    low = 0
    high = len(arr) - 1
    mid = 0
    exprFunc = lambda v: v
    statDict = {'Fulfilled':0, 'Receiving':1, 'Collecting':2, 'Pending':3}
    if modifier != "":
        exprFunc = eval('lambda v:' + f"{modifier}")
 
    while low <= high:
        mid = (high + low) // 2

        if exprFunc(arr[mid]) < x:        # If x is greater, ignore left half
            low = mid + 1
        elif exprFunc(arr[mid]) > x:      # If x is smaller, ignore right half
            high = mid - 1
        else:                   # means x is present at mid
            return mid
 
    # The element was not present
    return -1



MSG_QUEUE = []



def initGmailAPI():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            serv = ServiceAccountInfo.load()
            serv.serviceActive=False
            errs = serv.errorMessages
            errs["Initializing Gmail API failed since credentials file does not exist."] = True
            serv.errorMessages = errs
            serv.save()
            return None
            #flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            #creds = flow.run_local_server(port=8080)
        # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        # creds = flow.run_local_server(port=8080)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        gmailService = build('gmail', 'v1', credentials=creds)
        # REMOVED THE SERV SINGLETON UPDATE SINCE ONLY PLACE IT IS FIXED IS OAUTH2CALLBACK VIEW IN MAINPG. JUST UPDATING THE SINGLETON THERE
        # serv = ServiceAccountInfo.load()
        # serv.serviceActive = True
        # serv.errorMessages = {}
        # serv.save()


        # results = gmailService.users().labels().list(userId='me').execute()
        # labels = results.get('labels', [])

        # if not labels:
        #     print('No labels found.')
        #     return gmailService
        # print('Labels:')
        # for label in labels:
        #     print(label['name'])


        return gmailService

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        serv = ServiceAccountInfo.load()
        serv.serviceActive=False
        errs = serv.errorMessages
        errs[str(error)] = True
        serv.errorMessages = errs
        serv.save()
        return None




def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

    Returns:
    An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}



def send_message(service, user_id, message):
    """
    service: Authorized Gmail API service instance.
    user_id: Sender email address. Can use "me"
    message: Message to be sent.

    Returns Sent Message.

    send_message(GMAIL_SERVICE, 'me', create_message("me", "pranavcsomu@gmail.com", "TEST SUBJ", "TEST MSG"))
    """
    serv = ServiceAccountInfo.load()
    if not service:
        MSG_QUEUE.append([user_id, message])
        #ServiceActive and error message is already inserted from the initGmailAPIT function.
        serv.messageQueue = serv.messageQueue + [[user_id, message],]
        serv.save()
        return False
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        serv.serviceActive = True
        serv.errorMessages = {}
        serv.save()
        #print('Message Id: %s' % message['id'])
        return True
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        MSG_QUEUE.append([user_id, message])
        serv.serviceActive=False
        errs = serv.errorMessages
        errs[str(error)] = True
        serv.errorMessages = errs
        serv.messageQueue = serv.messageQueue + [[user_id, message],]
        serv.save()
        return False


def sendMsgQueue():
    while len(MSG_QUEUE) > 0:
        curmess = MSG_QUEUE.pop()
        #FIX THIS
        send_message(initGmailAPI(), curmess[0], curmess[1])




