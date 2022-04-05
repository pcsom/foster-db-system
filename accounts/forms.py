from django.forms import ModelForm, DateField, DateInput
from .models import child, userBasic


class userBasicForm(ModelForm):
    class Meta:
        model = userBasic
        fields = ('address', 'city', 'state', 'zipCode', 'county', 'cellPhone', 'homePhone', 'contactMethod', 'emailUpdateList', 'remindUpdateList')

    def __init__(self, *args, **kwargs):
        super(userBasicForm, self).__init__(*args, **kwargs)
        self.fields['address'].label = 'Address: *'
        self.fields['city'].label = 'City: *'
        self.fields['state'].label = 'State: *'
        self.fields['zipCode'].label = 'Zip Code: *'
        self.fields['county'].label = 'County: *'
        self.fields['cellPhone'].label = 'Cell Phone Number (Type the ten digit number, NO symbols): *'
        self.fields['homePhone'].label = 'Home Phone Number (Type the ten digit number, NO symbols): *'
        self.fields['contactMethod'].label = 'Preferred Method of Contact: *'
        self.fields['emailUpdateList'].label = 'Email Address Updates?'
        self.fields['remindUpdateList'].label = 'Remind (cell phone texts) Updates?'

        for oneField in self.fields.keys():
            if oneField not in ['contactMethod', 'emailUpdateList', 'remindUpdateList']:
                self.fields[oneField].initial = ''


class childForm(ModelForm):
    dateOfBirth = DateField(
        input_formats=['%m/%d/%Y'],
        widget=DateInput(format='%m/%d/%Y')
    )
    class Meta:
        model = child
        fields = ('firstName', 'gender', 'careType', 'newPlacement', 'dateOfBirth', 'clothesSize', 'shoeSize', 'specials', 'favorites', 'hasAllergy', 'allergyDescription')
    def __init__(self, *args, **kwargs):
        super(childForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].label = "First Name: *"
        self.fields['gender'].label = "Gender: *"
        self.fields['careType'].label = "Type (pick one): *"
        self.fields['newPlacement'].label = "Is this child new to your home (new placement)? : *"
        self.fields['dateOfBirth'].label = "Date of Birth (MM/DD/YYYY): *"
        #self.fields['dateOfBirth'].input_formats = ['%m/%d/%Y',]
        self.fields['clothesSize'].label = "Clothing Size: *"
        self.fields['shoeSize'].label = "Shoe Size: *"
        self.fields['specials'].label = "Special needs/considerations:"
        self.fields['favorites'].label = "Favorite types of items/characters (i.e. Frozen, Paw Patrol):"
        self.fields['hasAllergy'].label = "Does this child have any material allergies (i.e. needs 100% cotton, certain brand of diapers)?"
        self.fields['allergyDescription'].label = "Please describe allergies: *"
        self.fields['allergyDescription'].required = False
        
        for oneField in self.fields.keys():
            if oneField not in ['age', 'careType', 'hasAllergy', 'specials', 'favorites', 'allergyDescription']:
                self.fields[oneField].initial = ''