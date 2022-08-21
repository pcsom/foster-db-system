
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utility import processName
from django.core.exceptions import ValidationError
from .models import *
from utility import getFieldsOfType
from django.db.models import TextField
from mainpg.models import ReqFormSettings


"""@receiver(post_save, sender=itemsRequest)
def updateReqDescs(sender, instance, **kwargs):
    for field in getFieldsOfType(instance, TextField).keys():
        dataStr = getattr(instance, field)
        nl = '\n'
        sym = ';:,!?.'
        try:
            if nl in dataStr:
                newStr = '. '.join([item.strip()[0:-1] if item.strip()[-1] in sym else item.strip() for item in dataStr.split(nl)]) + '.'
                setattr(instance, field, newStr)
        except TypeError as e:
            pass"""

@receiver(pre_save, sender=itemsRequest)
def correctFieldsRequests(instance, **kwargs):
    # curVals = to_dict(instance)
    # for one in curVals.keys():
    #     if curVals[one] == '':
    #         raise ValidationError(f"Attempted to save, but field '{processName(one)}' was invalid.")
    
    # curData = json.loads(instance.formData)
    # newData = {}
    # for i in curData:
    #     if curData[i] not in [False, "", None]:
    #         newData[i] = curData[i]
    # instance.formData = newData
    
    instance.full_clean()

    sett = ReqFormSettings.load()
    curLinks = sett.links
    databaseDisplay = sett.databaseDisplay

    
    formData = instance.formData
    if isinstance(formData, str):
        formData = json.loads(formData)
    errdict = {}
    for field in curLinks:
        if field in formData:
            for linked in curLinks[field]:
                if linked not in formData:
                    errStr = f"Field \"{databaseDisplay[linked]}\" is required if you fill out field \"{databaseDisplay[field]}\""
                    if field in errdict:
                        errdict[field].append(errStr)
                    else:
                        errdict[field] = [errStr,]
        else:
            for linked in curLinks[field]:
                if linked in formData:
                    del formData[linked]


    if len(errdict) > 0:
        raise ValidationError(errdict)
    
    if len(formData) == 0:
        raise Exception("Form cannot be blank.")


    instance.formData = formData
                


    dataStr = getattr(instance, "formData")
    nl = '\n'
    sym = ';:,!?.'
    if nl in dataStr:
        newStr = '. '.join([item.strip()[0:-1] if item.strip()[-1] in sym else item.strip() for item in dataStr.split(nl)]) + '.'
        setattr(instance, "formData", newStr)

    

