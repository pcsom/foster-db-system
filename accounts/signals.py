
from accounts.forms import userBasicForm
from typing import Text
from django.db.models.functions.math import Mod
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utility import *
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from .models import *
from django.db.models.fields import TextField
import json
from datetime import date


@receiver(pre_save, sender=User)
def uniqueFields(sender, instance, **kwargs):
    isErr = False
    errDict = {}
    mess = "Another user already has the provided "
    if not uniqueEmail(instance, instance.email):
        isErr = True
        errDict['email'] = ["Another user already has the provided email.",]
    
    if not uniqueUsername(instance, instance.username):
        isErr = True
        errDict['username'] = ["Another user already has the provided username.",]

    if isErr:
        raise ValidationError(errDict)
    
    

@receiver(pre_save, sender=child)
@receiver(pre_save, sender=adoptiveFamily)
@receiver(pre_save, sender=kinshipFamily)
@receiver(pre_save, sender=fosterFamily)
@receiver(pre_save, sender=safetyFamily)
def updateChildDescs(sender, instance, **kwargs):
    for field in getFieldsOfType(instance, TextField).keys():
        dataStr = getattr(instance, field)
        if dataStr and '\n' in dataStr:
            if dataStr[-1] == '\n':
                dataStr = dataStr[:-1]
            newStr = '. '.join([item.strip()[0:-1].replace("\r", "") if item.strip()[-1] in ';:,!?.' else item.strip() for item in dataStr.split('\n')]) + '.'
            setattr(instance,field, newStr)




@receiver(pre_save, sender=userBasic)
@receiver(pre_save, sender=child)
@receiver(pre_save, sender=careType)
@receiver(pre_save, sender=adoptiveFamily)
@receiver(pre_save, sender=kinshipFamily)
@receiver(pre_save, sender=fosterFamily)
@receiver(pre_save, sender=safetyFamily)
def correctFieldsAccounts(sender, instance, **kwargs):
    # curVals = to_dict(instance)
    # for one in curVals.keys():
    #     if curVals[one] == '':
    #         raise ValidationError(f"Attempted to save, but field '{processName(one)}' was invalid.")
    if sender == child:
        today = date.today()
        instance.age = today.year - instance.dateOfBirth.year - ((today.month, today.day) < (instance.dateOfBirth.month, instance.dateOfBirth.day))
    instance.full_clean()


#add post save update column w/ str form of data

@receiver(post_save, sender=User)
def updateDataTableInfo_User(sender, instance, **kwargs):
    if instance.id is None:
        return
    try:
        theBasic = userBasic.objects.get(user=instance)
        theBasic.save()
    except:
        return

@receiver(pre_save, sender=userBasic)
def updateDataTableInfo(sender, instance, **kwargs):
    if instance.id is None:
        return
    toManage = instance.user
    numReqs = toManage.itemsrequest_set.count()
    numChild = toManage.child_set.count()
    finalDict = dict()

    if toManage.username == "None":
        finalDict = {'edit': False, 'result':["None",], 'id':toManage.id, 'numChild':numChild, 'numReqs': numReqs}
    else:
        careInfo = []
        try:
            curCare = toManage.caretype
            careInfo = [curCare.adoptive, curCare.foster, curCare.kinship, curCare.safety]
        except ObjectDoesNotExist:
            careInfo = ["UNSET" for i in range(4)]
        
        userBasicList = getVals(instance, exclude=['user', 'registrationProgress', 'id'], display=['contactMethod'])
        fullList = [toManage.username, toManage.first_name, toManage.last_name, toManage.email] + userBasicList + [numChild, careInfo.count(True), careInfo[0], careInfo[1], careInfo[2], careInfo[3], numReqs]
        finalDict = {'edit': True, 'result':fullList, 'id':toManage.id}
    instance.dataTableInfo = finalDict



@receiver(pre_save, sender=child)
def updateDataTabInfoChild(sender, instance, **kwargs):
    if instance.id is None:
        return
    numReqs = instance.itemsrequest_set.count()

    if not instance.hasAllergy:
        instance.allergyDescription = None

    finalDict = {
        'edit': instance != child.objects.get(firstName="None"),
        'result': getVals(instance, objField={'parent': '__str__()'}, formatDate=["dateOfBirth",], exclude=['id', ]) + [numReqs,],
        'id':instance.id
    }
    

    instance.dataTableInfo = finalDict




@receiver(pre_save, sender=careType)
def setName(sender, instance, **kwargs):
    instance.name = str(instance.user)