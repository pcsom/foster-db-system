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
    address = models.CharField(max_length=100, default="Unset")                  #for an image, u need to put a path. use models.ImageField(upload_to='folder_with_pictures')
    city = models.CharField(max_length=50, default="Unset")                     #change all the colons into equal signs
    state = models.CharField(max_length=30, default="Unset")
    zipCode = models.IntegerField(default=0)
    county = models.CharField(max_length=50, default="USA")
    cellPhone = models.BigIntegerField(default=0)
    homePhone = models.BigIntegerField(default=0)
    contactMethod = models.CharField(max_length=50, default="emailRadio", choices=CONTACTMETHOD)
    emailUpdateList = models.BooleanField(default=False)
    remindUpdateList = models.BooleanField(default=False)
    registrationProgress = models.CharField(max_length=50, default='Complete')

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

    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('unspecified', 'Prefer not to specify'),
    )

    CLOTHEGENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('nopref', 'No preference'),
    )

    CLOTHESIZES = (
        ('preemie', 'Preemie'),
        ('nb', 'NB'),
        ('0-3m', '0-3m'),
        ('3m', '3m'),
        ('3-6m', '3-6m'),
        ('6m', '6m'),
        ('6-9m', '6-9m'),
        ('9m', '9m'),
        ('9-12m', '9-12m'),
        ('12m', '12m'),
        ('12-18m', '12-18m'),
        ('18m', '18m'),
        ('18-24m', '18-24m'),
        ('24m', '24m'),
        ('2t', '2t'),
        ('3t', '3t'),
        ('4t', '4t'),
        ('5t', '5t'),
        ('4/5', '4/5'),
        ('5', '5'),
        ('5/6', '5/6'),
        ('6', '6'),
        ('6/7', '6/7'),
        ('7', '7'),
        ('7/8', '7/8'),
        ('8', '8'),
        ('8/10', '8/10'),
        ('10', '10'),
        ('10/12', '10/12'),
        ('12', '12'),
        ('12/14', '12/14'),
        ('14', '14'),
        ('14/16', '14/16'),
        ('16', '16'),
        ('16/18', '16/18'),
        ('18', '18'),
        ('adultSmall', 'Adult Small'),
        ('adultMedium', 'Adult Medium'),
        ('adultLarge', 'Adult Large'),
        ('adultXLarge', 'Adult X Large'),
        #('adult', 'Adult (on request form, specify size in field \"Please list any other needs\"'),
    )
    
    parent = models.ForeignKey(User, default=User.objects.get(username="None").pk, on_delete=models.SET_DEFAULT)
    
    firstName = models.CharField(max_length=50, default="Unset")
    gender = models.CharField(max_length=40, default="unspecified", choices=GENDER)
    clothingGender = models.CharField(max_length=40, default="nopref", choices=CLOTHEGENDER)
    careType = models.CharField(max_length=15, default="adopted", choices=TYPE)
    newPlacement = models.CharField(max_length=5, default="No", choices=PLACEMENT)
    relationship = models.CharField(max_length=30, default="Unset")
    age = models.IntegerField(default=0)
    dateOfBirth = models.DateField(default=date(2000,1,1))      #models.CharField(max_length=300, default="Unset")
    clothesSize = models.CharField(max_length=50, default="preemie", choices=CLOTHESIZES)
    shoeSize = models.CharField(max_length=100, default="Unset")
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
    name = models.CharField(max_length=100, null=True)

    adoptive = models.BooleanField(default=False)
    foster = models.BooleanField(default=False)
    kinship = models.BooleanField(default=False)
    safety = models.BooleanField(default=False)

    signature = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateField(default=date(2000,1,1))    #change if needed, default to 1/1/2000

    def __str__(self):
        return self.name

class adoptiveFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

class fosterFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    county = models.CharField(max_length=50, default="Unset")
    agency = models.CharField(max_length=70, default="Unset")
    workerName = models.CharField(max_length=100, default="Unset")
    workerContact = models.TextField(max_length=100, default="Unset")

    def __str__(self):
        return str(self.user)

class kinshipFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    placementRelation = models.TextField(max_length=100, default="Unset")
    county = models.CharField(max_length=50, default="Unset")
    workerName = models.CharField(max_length=100, default="Unset")
    workerContact = models.TextField(max_length=100, default="Unset")

    def __str__(self):
        return str(self.user)

class safetyFamily(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    county = models.CharField(max_length=50, default="Unset")
    planTimeLength = models.TextField(max_length=100, default="Unset")
    workerName = models.CharField(max_length=100, default="Unset")
    workerContact = models.TextField(max_length=100, default="Unset")

    def __str__(self):
        return str(self.user)



class UserAdmin(AuthUserAdmin):
    inlines = [userBasicInline,]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
