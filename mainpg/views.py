from django.db.models.fields import BigIntegerField
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from accounts.models import *
from django.contrib.auth.decorators import login_required
from decorators import allowed_users
from django.core.mail import send_mail
from utility import *
from irequests.forms import itemsRequestForm
from django.contrib import messages

import os

from google.auth.transport.requests import Request
from nafc.settings import BASE_URL
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.mime.text import MIMEText
from .models import *
from adminManagement.models import *
from django.urls import reverse
from nafc.settings import BASE_URL
import subprocess
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
import traceback
import logging
log = logging.getLogger(__name__)
# Create your views here.


def java_script(request):
    print("in js")
    filename = request.path.strip("/")
    data = open(filename, "rb").read()
    return HttpResponse(data, mimetype="text/javascript")





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin', 'user'])
def index(request):
    #remember the none user and none child creation lines
    # userNone = User.objects.get(username="None")
    # userBasic.objects.create(user=userNone, address="None", city="None", state="None", county="None")
    # userNone.first_name = ""
    # userNone.last_name = ""
    # userNone.save()
    

    group = None
    curUser = request.user
    if curUser.groups.exists():
        group = curUser.groups.all()[0].name

    children = child.objects.filter(parent=curUser).all()
    currentCareType = careType.objects.filter(user=curUser).first()
    basicInfo = curUser.userbasic

    
    isAdmin = "False"
    if group=='admin':
        isAdmin = "True"

    # THE BELOW IS OUTDATED!!!! THE DISPLAY NAME HAS BEEN REMOVED; IT IS INSTEAD STORED IN A SEPARATE VAR "databaseDisplay"
    # sett = ReqFormSettings.load()
    # sett.fieldInfo = [
    #     ['Infant Items', [
    #             ['onesies', 'Onesies', 'boolean'], 
    #             ['twoPieceOutfits', 'Two Piece Outfits', 'boolean'],
    #             ['sleepSack', 'Sleep Sack', 'boolean'],
    #             ['cribSheets', 'Crib Sheets', 'boolean'],
    #             ['crib', 'Crib', 'boolean'],
    #             ['bibs', 'Bibs', 'boolean'],
    #             ['receivingBlankets', 'Recieving Blankets', 'boolean'],
    #             ['burpCloths', 'Burp Cloths', 'boolean'],
    #             ['bottles', 'Bottles', 'boolean'],
    #             ['stroller', 'Stroller', 'boolean'],
    #             ['strollerType', 'Stroller Type', 'dropdown', ['Single', 'Double']],       #Ad custom choice field
    #             ['formula', 'Formula', 'boolean'],
    #             ['formulaType', 'Formula Type', 'char'],
    #             ['diapers', 'Diapers', 'boolean'],
    #             ['diapersSize', 'Diapers Size', 'char'],
    #             ['wipes', 'Wipes', 'boolean'],
    #             ['otherInfantNeeds', 'Please describe any other infant needs.', 'boolean'],
    #         ]
    #     ],
    #     ['Child Items', [
    #             ['shortSleeveShirts', 'Short Sleeve Shirts', 'boolean'],
    #             ['longSleeveShirts', 'Long Sleeve Shirts', 'boolean'],
    #             ['shorts', 'Shorts', 'boolean'],
    #             ['longPants', 'Long Pants', 'boolean'],
    #             ['pajamas', 'Pajamas', 'boolean'],
    #             ['dressClothes', 'Dress Clothes', 'boolean'],
    #             ['dresses', 'Dresses', 'boolean'],
    #             ['winterCoats', 'Winter Coats', 'boolean'],
    #             ['swimwear', 'Swimwear', 'boolean'],
    #             ['holidayOutfit', 'Holiday Outfit', 'boolean'],
    #             ['shoes', 'Shoes', 'boolean'],
    #         ]
    #     ],
    #     ['Toiletries', [
    #             ['toothbrush', 'Toothbrush', 'boolean'],
    #             ['toothpaste', 'Toothpaste', 'boolean'],
    #             ['deodorant', 'Deodorant', 'boolean'],
    #             ['soap', 'Soap', 'boolean'],
    #             ['shampoo', 'Shampoo', 'boolean'],
    #             ['ethnicHairCareProducts', 'Ethnic Hair Care Products', 'boolean'],
    #             ['hairAccessories', 'Hair Accessories', 'boolean'],
    #             ['makeUpItems', 'Make Up Items', 'boolean'],
    #             ['makeUpItemsDescription', 'Please describe the needed make-up items.', 'char'],
    #         ]
    #     ],
    #     ['General', [
    #             ['schoolSupplies', 'Please list any needed school supplies.', 'char'],
    #             ['toysGamesBooks', 'Please list any needed toys, games, or books.', 'char'],
    #             ['bedding', 'Please list any needed bedding items.', 'char'],
    #             ['weightedBlanket', 'Weighted Blanket', 'char'],
    #             ['otherNeeds', 'Please list any other needs.', 'char'],
    #         ]
    #     ],
    # ]
    # sett.save()
    #with open('debug.log', 'w') as outf:
    #    proc = subprocess.Popen(["systemctl", "daemon-reload"], stdout=outf)
    #    proc = subprocess.Popen(["systemctl", "restart", "gunicorn"], stdout=outf)
    #    try:
    #        outs, errs = proc.communicate(timeout=15)
    #        log.debug(f"{outs}")
    #        log.debug(f"{errs}")
    #    except Exception as e:
    #        proc.kill()
    #        outs, errs = proc.communicate()
    #        log.debug(f"{outs}")
    #        log.debug(f"{errs}")

    context = {
        'children': children, 'basicInfo': basicInfo, 'curUser': curUser, 
        'currentCareType': currentCareType, 'admin': isAdmin,
    }
    

    return render(request, 'userDash.html', context)

def contact(request):
    return render(request, "contact.html")



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin',])
def authAccount(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file("credentials.json", scopes=SCOPES)
    flow.redirect_uri = f'{BASE_URL}/oauth2callback'
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true', prompt='consent')
    gmailAPI = initGmailAPI()
    emailError = True
    if gmailAPI:
        emailError = False
    serv = ServiceAccountInfo.load()
    errList = list(serv.errorMessages.keys())
    if emailError:
        serv.serviceActive = False
    serv.save()
    context = {'authLink':authorization_url, 'authError':emailError, 'errList':errList}
    return render(request, 'admin/authAccount.html', context)


def OAuth2CallBack(request):
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    state = request.GET['state']
    basepath = os.path.dirname(__file__)
    filepath = os.path.abspath(os.path.join(basepath, "..", "credentials.json"))
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(filepath, scopes=SCOPES, state=state)
    flow.redirect_uri = f"{BASE_URL}/oauth2callback"
    
    code=request.GET['code']
    flow.fetch_token(code=code)
    creds = flow.credentials
    with open(os.path.join(basepath, "..", "token.json"), 'w') as token:
        token.write(creds.to_json())

    serv = ServiceAccountInfo.load()
    gmailServ = initGmailAPI()
    if gmailServ:
        serv.serviceActive = True
        serv.errorMessages = {}
        msgs = serv.messageQueue
        serv.messageQueue = []
        serv.save()
        for i in msgs:
            send_message(gmailServ, i[0], i[1])
        #os.system("sudo systemctl restart nginx")
        #try:
        #    subprocess.run(["systemctl", "restart", "nginx"])
        #except Exception as e:
        #    print(traceback.format_exc())

        proc = subprocess.Popen(["systemctl", "daemon-reload"])
        proc = subprocess.Popen(["systemctl", "restart", "gunicorn"])
        messages.success(request, "Google OAuth token attained successfully")
    else:
        messages.error(request, "Google OAuth still is out of order.")



    return redirect('/')

