from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from accounts.models import child
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from datetime import date
from utility import processName


class itemsRequest(models.Model):
    forChild = models.ForeignKey(child, default=child.objects.get(firstName="None").pk, on_delete=models.SET_DEFAULT)
    forUser = models.ForeignKey(User, default=User.objects.get(username="None").pk, on_delete=models.SET_DEFAULT, db_index=True)
    preferredMethodOfReceiving = models.JSONField(null=True, blank=True)
    date = models.DateField(default=date.today)
    status = models.CharField(default="Pending", max_length=20)

    STROLLER_TYPE = (
        ('double', 'Double'),
        ('single', 'Single'),
    )

    #Infant items
    onesies = models.BooleanField(default=False)
    twoPieceOutfits = models.BooleanField(default=False)
    sleepSack = models.BooleanField(default=False)
    cribSheets = models.BooleanField(default=False)
    crib = models.BooleanField(default=False)
    bibs = models.BooleanField(default=False)
    receivingBlankets = models.BooleanField(default=False)
    burpCloths = models.BooleanField(default=False)
    washcloths = models.BooleanField(default=False)
    bottles = models.BooleanField(default=False)
    stroller = models.BooleanField(default=False)
    strollerType = models.CharField(null=True, blank=True, choices=STROLLER_TYPE, max_length=20)
    formula = models.BooleanField(default=False)
    formulaType = models.CharField(null=True, blank=True, max_length=100)
    diapers = models.BooleanField(default=False)
    diapersSize = models.CharField(null=True, blank=True, max_length=100)
    wipes = models.BooleanField(default=False)
    otherInfantNeeds = models.TextField(null=True, blank=True)

    #Children/teen
    shortSleeveShirts = models.BooleanField(default=False)
    longSleeveShirts = models.BooleanField(default=False)
    shorts = models.BooleanField(default=False)
    longPants = models.BooleanField(default=False)
    pajamas = models.BooleanField(default=False)
    dressClothes = models.BooleanField(default=False)
    dresses = models.BooleanField(default=False)
    winterCoats = models.BooleanField(default=False)
    swimwear = models.BooleanField(default=False)
    holidayOutfit = models.BooleanField(default=False)
    shoes = models.BooleanField(default=False)

    #Toiletries
    toothbrush = models.BooleanField(default=False)
    toothpaste = models.BooleanField(default=False)
    deodorant = models.BooleanField(default=False)
    soap = models.BooleanField(default=False)
    shampoo = models.BooleanField(default=False)
    ethnicHairCareProducts = models.BooleanField(default=False)
    hairAccessories = models.BooleanField(default=False)
    makeUpItems = models.BooleanField(default=False)
    makeUpItemsDescription = models.TextField(null=True, blank=True)
    
    #School Supplies
    schoolSupplies = models.TextField(null=True, blank=True)

    #Toys/Games/Books
    toysGamesBooks = models.TextField(null=True, blank=True)

    #Bedding Furniture/items
    bedding = models.TextField(null=True, blank=True)

    #Weighted Blanket
    weightedBlanket = models.BooleanField(default=False)

    #Other needs
    otherNeeds = models.TextField(null=True, blank=True)


    def getStatus(self):
        return f"({self.status[0]})"
            

    #All basic info
    def __str__(self):
        return f"{self.getStatus()} {self.forUser}'s Request for {self.forChild} on {self.date.strftime('%m/%d/%Y')}"

    #Esxclude user's name
    def childDateInfo(self):
        return f"{self.getStatus()} Request for {self.forChild} on {self.date.strftime('%m/%d/%Y')}"

    #Get all values in the request (essentially, the requested items)
    def get_fields(self, strDate=False):
        allfields = [(processName(field.name), getattr(self, field.name)) for field in itemsRequest._meta.fields]
        theDate = self.date
        if strDate:
            theDate = str(theDate)
        finalfields = {"name": self.__str__(), "childDateInfo": self.childDateInfo(), "receiving": allfields[3][1], "date": theDate, "fields": []}
        for name, value in allfields[6:]:
            if value and value != 'False':
                newVal = ": " + str(value)
                if newVal == ': True':
                    newVal = " "
                finalfields['fields'].append((name, newVal))

        return finalfields

