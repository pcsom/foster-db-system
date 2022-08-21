
from typing import final
from django.db.models.signals import post_save, pre_save, pre_delete
from django.dispatch import receiver
from utility import processName, getFieldsOfType, getVals
from django.core.exceptions import ValidationError
from .models import *
from django.db.models import TextField



@receiver(pre_save, sender=donorEntry)
def updateChildDescs(sender, instance, **kwargs):
    for field in getFieldsOfType(instance, TextField).keys():
        #dataStr = eval(f"instance.{field}")
        dataStr = getattr(instance, field)
        nl = '\n'
        sym = ';:,!?.'
        if nl in dataStr:
            newStr = '. '.join([item.strip()[0:-1] if item.strip()[-1] in sym else item.strip() for item in dataStr.split(nl)]) + '.'
            #exec(f"instance.{field} = newStr")
            setattr(instance, field, newStr)


@receiver(pre_save, sender=hoursEntry)
@receiver(pre_save, sender=distributionEntry)
@receiver(pre_save, sender=donorEntry)
@receiver(pre_save, sender=volunteer)
def correctFieldsAdmin(sender, instance, **kwargs):
    # curVals = to_dict(instance)
    # for one in curVals.keys():
    #     if curVals[one] == '':
    #         raise ValidationError(f"Attempted to save, but field '{processName(one)}' was invalid.")
    if sender == hoursEntry:
        if instance.hoursWorked <= 0:
            raise ValidationError({'hoursWorked': 'Enter a value greater than 0'})
    instance.full_clean()
    finalDict = {}

    if sender == distributionEntry:
        finalDict = {
            'result': getVals(instance, formatDate=['dateDistributed',], exclude=['id',], objField={'forChild': '__str__()'}, formatBool=['sent',]),
            'id':instance.id
        }

    elif sender == donorEntry:
        finalDict = {
            'result': getVals(instance, exclude=['id',]),
            'id':instance.id
        }

    elif sender == volunteer:
        finalDict = {
            'edit': True,
            'result': getVals(instance, exclude=['id',], applyFunc={'totalHoursWorked': 'float'}),
            'id':instance.id
        }
        if instance == volunteer.objects.get(name="Global Volunteer Hour Count"):
            finalDict['edit'] = False

    elif sender == hoursEntry:
        finalDict = {
            'result': getVals(instance, formatDate=['date',], exclude=['id',], objField={'forVolunteer': 'name'}, applyFunc={'hoursWorked': 'float'}),
            'id':instance.id
        }

    instance.dataTableInfo = finalDict


# @receiver(pre_save, sender=hoursEntry)
# def hoursAddChangeGlobal(sender, instance, **kwargs):
#     globObj = volunteer.objects.get(name="Global Volunteer Hour Count")

#     if instance.pk:
#         pass
#     else:
#         globObj.totalHoursWorked += instance.hoursWorked
