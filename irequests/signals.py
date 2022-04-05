
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from utility import processName
from django.core.exceptions import ValidationError
from .models import *
from utility import getFieldsOfType
from django.db.models import TextField


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
    instance.full_clean()

    for field in getFieldsOfType(instance, TextField).keys():
        dataStr = getattr(instance, field)
        nl = '\n'
        sym = ';:,!?.'
        try:
            if nl in dataStr:
                newStr = '. '.join([item.strip()[0:-1] if item.strip()[-1] in sym else item.strip() for item in dataStr.split(nl)]) + '.'
                setattr(instance, field, newStr)
        except TypeError as e:
            pass

    

