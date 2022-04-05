from operator import truediv
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from datetime import date

# Create your models here.

def get_name(self):
    return f"{self.first_name} {self.last_name} ({self.username})"

User.add_to_class("__str__", get_name)



class userBasic(models.Model):
    CONTACTMETHOD = (
        ('cellPhRadio', 'Cell Phone Number'),
        ('homePhRadio', 'Home Phone Number'),
        ('emailRadio', 'Email Address'),
    )
    
    user = models.OneToOneField(User, null=True, blank=True, default=None, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, default="Unset")                  #for an image, u need to put a path. use models.ImageField(upload_to='folder_with_pictures')
    city = models.CharField(max_length=300, default="Unset")                     #change all the colons into equal signs
    state = models.CharField(max_length=300, default="Unset")
    zipCode = models.IntegerField(default=0)
    county = models.CharField(max_length=300, default="USA")
    cellPhone = models.BigIntegerField(default=0)
    homePhone = models.BigIntegerField(default=0)
    contactMethod = models.CharField(max_length=300, default="emailRadio", choices=CONTACTMETHOD)
    emailUpdateList = models.BooleanField(default=False)
    remindUpdateList = models.BooleanField(default=False)
    registrationProgress = models.CharField(max_length=300, default='Complete')

    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)
    
    def __str__(self):
        return str(self.user)


class userBasicInline(admin.StackedInline):
    model = userBasic

class child(models.Model):
    TYPE = (
        ('biological', 'Biological'),
        ('adopted', 'Adopted'),
        ('foster', 'Foster'),
        ('kinship', 'Kinship'),
        ('safety-plan', 'Safety-plan'),
        ('respite', 'Respite'),
    )

    PLACEMENT = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    
    parent = models.ForeignKey(User, default=User.objects.get(username="None").pk, on_delete=models.SET_DEFAULT)
    
    firstName = models.CharField(max_length=300, default="Unset")
    gender = models.CharField(max_length=300, default="Unset")
    careType = models.CharField(max_length=300, default="adopted", choices=TYPE)
    newPlacement = models.CharField(max_length=300, default="Unset", choices=PLACEMENT)
    age = models.IntegerField(default=0)
    dateOfBirth = models.DateField(default=date(2000,1,1))      #models.CharField(max_length=300, default="Unset")
    clothesSize = models.CharField(max_length=300, default="Unset")
    shoeSize = models.CharField(max_length=300, default="Unset")
    specials = models.TextField(null=True, blank=True)
    favorites = models.TextField(null=True, blank=True)
    hasAllergy = models.BooleanField(default=False)
    allergyDescription = models.TextField(null=True, blank=True)


    def buildDefDict():
        return dict(edit=False, result=['SYSTEM ERROR - Data table information has not been configured',], id=-1)
    dataTableInfo = models.JSONField(default=buildDefDict)

    def __str__(self):
        return self.firstName



'''
class childInline(admin.StackedInline):
    model = child
    fk_name = 'parent'
'''


class careType(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=300, null=True)

    adoptive = models.BooleanField(default=False)
    foster = models.BooleanField(default=False)
    kinship = models.BooleanField(default=False)
    safety = models.BooleanField(default=False)

    signature = models.CharField(max_length=300, null=True, blank=True)
    date = models.CharField(max_length=300, null=True, blank=True)    #change if needed, default to 1/1/2000

    def __str__(self):
        return self.name

class adoptiveFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    adoptedChildren = models.TextField(default="Unset")

    def __str__(self):
        return str(self.user)

class fosterFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    county = models.CharField(max_length=300, default="Unset")
    agency = models.CharField(max_length=300, default="Unset")
    workerName = models.CharField(max_length=300, default="Unset")
    workerContact = models.TextField(max_length=300, default="Unset")

    def __str__(self):
        return str(self.user)

class kinshipFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    children = models.TextField(default="Unset")
    placementRelation = models.TextField(max_length=500, default="Unset")
    county = models.CharField(max_length=300, default="Unset")
    workerName = models.CharField(max_length=300, default="Unset")
    workerContact = models.TextField(max_length=300, default="Unset")

    def __str__(self):
        return str(self.user)

class safetyFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    county = models.CharField(max_length=300, default="Unset")
    planTimeLength = models.TextField(max_length=500, default="Unset")
    workerName = models.CharField(max_length=300, default="Unset")
    workerContact = models.TextField(max_length=300, default="Unset")

    def __str__(self):
        return str(self.user)



class UserAdmin(AuthUserAdmin):
    inlines = [userBasicInline,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
