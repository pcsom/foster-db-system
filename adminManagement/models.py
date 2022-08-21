from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import child
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from datetime import date
from utility import *

# class distributionEntry(models.Model):
#     #forFamily = models.ForeignKey(User, default=User.objects.get(username="None").pk, on_delete=models.SET_DEFAULT)
#     forChild = models.ForeignKey(child, default=child.objects.get(firstName="None").pk, on_delete=models.SET_DEFAULT)
#     dateDistributed = models.DateField(default=date.today)
#     sent = models.BooleanField(default=False)

#     #Infant items
#     onesies = models.PositiveIntegerField(default=0)
#     twoPieceOutfits = models.PositiveIntegerField(default=0)
#     sleepSack = models.PositiveIntegerField(default=0)
#     cribSheets = models.PositiveIntegerField(default=0)
#     crib = models.PositiveIntegerField(default=0)
#     bibs = models.PositiveIntegerField(default=0)
#     receivingBlankets = models.PositiveIntegerField(default=0)
#     burpCloths = models.PositiveIntegerField(default=0)
#     washcloths = models.PositiveIntegerField(default=0)
#     bottles = models.PositiveIntegerField(default=0)
#     stroller = models.PositiveIntegerField(default=0)
#     formula = models.PositiveIntegerField(default=0)
#     diapers = models.PositiveIntegerField(default=0)
#     wipes = models.PositiveIntegerField(default=0)
#     furniture = models.PositiveIntegerField(default=0)

#     #Children/teen
#     shortSleeveShirts = models.PositiveIntegerField(default=0)
#     longSleeveShirts = models.PositiveIntegerField(default=0)
#     shorts = models.PositiveIntegerField(default=0)
#     longPants = models.PositiveIntegerField(default=0)
#     pajamas = models.PositiveIntegerField(default=0)
#     dressClothes = models.PositiveIntegerField(default=0)
#     dresses = models.PositiveIntegerField(default=0)
#     winterCoats = models.PositiveIntegerField(default=0)
#     swimwear = models.PositiveIntegerField(default=0)
#     shoes = models.PositiveIntegerField(default=0)


#     #Toiletries
#     toothbrush = models.PositiveIntegerField(default=0)
#     toothpaste = models.PositiveIntegerField(default=0)
#     deodorant = models.PositiveIntegerField(default=0)
#     soap = models.PositiveIntegerField(default=0)
#     shampoo = models.PositiveIntegerField(default=0)
#     ethnicHairCairProducts = models.PositiveIntegerField(default=0)
#     hairAccessories = models.PositiveIntegerField(default=0)
#     makeUpItems = models.PositiveIntegerField(default=0)
    

#     #School Supplies
#     schoolSupplies = models.PositiveIntegerField(default=0)

#     #Toys/Games/Books
#     toys = models.PositiveIntegerField(default=0)
#     games = models.PositiveIntegerField(default=0)
#     books = models.PositiveIntegerField(default=0)

#     #Bedding Furniture/items
#     bedding = models.PositiveIntegerField(default=0)

#     #Weighted Blanket
#     weightedBlanket = models.PositiveIntegerField(default=0)

    
#     def buildDefDict():
#         return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
#     dataTableInfo = models.JSONField(default=buildDefDict)


#     def __str__(self):
#         return f"Log for {self.forFamily} on {self.dateDistributed}"





class distributionEntry(models.Model):
    #forFamily = models.ForeignKey(User, default=User.objects.get(username="None").pk, on_delete=models.SET_DEFAULT)
    forChild = models.ForeignKey(child, default=child.objects.get(firstName="None").pk, on_delete=models.SET_DEFAULT)
    dateDistributed = models.DateField(default=date.today)
    sent = models.BooleanField(default=False)

    #Data table info would be redundant. Try seeing if can just make dataTableInfo for the three fields above?
    formData = models.JSONField(null=True,blank=True)

    
    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)


    def __str__(self):
        return f"Log for {child.objects.filter(id=self.forChild).parent} on {self.dateDistributed}"





class donorEntry(models.Model):
    name = models.CharField(default="Unset", max_length=300)
    emailAddress = models.EmailField(default="UNSET@UNSET.UNSET", max_length=300)
    mailingAddress = models.CharField(default="Unset", max_length=300)
    itemsDonated = models.TextField(null=True, blank=True)

    
    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)
        
    def __str__(self):
        return f"Donation by {self.name}"



class volunteer(models.Model):
    name = models.CharField(default="Unset", max_length=300)
    totalHoursWorked = models.DecimalField(default=0, max_digits=7, decimal_places=2)
    
    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)

    def updateVolHours(self):
        records = hoursEntry.objects.filter(forVolunteer=self).all()
        sum = 0
        for record in records:
            sum += record.hoursWorked
        self.totalHoursWorked = sum

        self.save()
            

    def __str__(self):
        return self.name



def rectifyGlobalVolHours():        #Will sum all hours log entries to get the global volunteer hours count; use if somehow the count has become wrong
    globObj = volunteer.objects.get(name="Global Volunteer Hour Count")
    hoursEntries = hoursEntry.objects.all()
    grandTotal = 0
    for entry in hoursEntries:
        grandTotal += entry.hoursWorked
    globObj.totalHoursWorked = grandTotal
    globObj.save()




class hoursEntry(models.Model):
    date = models.DateField(default=date.today)
    forVolunteer = models.ForeignKey(volunteer, default=volunteer.objects.get(name="Global Volunteer Hour Count").pk, on_delete=models.SET_DEFAULT)
    hoursWorked = models.DecimalField(default=0, max_digits=7, decimal_places=2)

    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)
    
    def __str__(self):
        return f"{self.forVolunteer.name} on {self.date.strftime('%m/%d/%Y')}"
