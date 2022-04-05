from django.forms import ModelForm, SelectDateWidget
from .models import *
from accounts.models import child
from utility import *



class distributionForm(ModelForm):
    class Meta:
        model = distributionEntry
        fields = (
            'dateDistributed',
            'onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
            'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller',
            'formula', 'diapers', 'wipes',  

            'shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
            'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'shoes', 

            'toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 'ethnicHairCairProducts', 
            'hairAccessories', 'makeUpItems', 
            
            'schoolSupplies', 'toys', 'games', 'books', 'bedding', 'bedding', 'weightedBlanket')
    


    def __init__(self, *args, **kwargs):        
        super(distributionForm, self).__init__(*args, **kwargs)
        
        self.fields['dateDistributed'].label = "Please enter the date these items were distributed: *"
        #self.fields['dateDistributed'].widget = SelectDateWidget()
        self.fields['dateDistributed'].input_formats = ['%m/%d/%Y']
        self.fields['dateDistributed'].initial = date.today().strftime("%m/%d/%Y")

        #Infants
        infantFields = ['onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
            'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 
            'formula', 'diapers', 'wipes']
        for field in infantFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'infant'}
              

        #Child/teen
        childFields = ['shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
            'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'shoes']
        for field in childFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'child'}


        #Toiletries
        toiletriesFields = ['toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 
            'ethnicHairCairProducts', 'hairAccessories', 'makeUpItems']
        for field in toiletriesFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'toiletries'}
    

        #General Fields
        generalFields = ['schoolSupplies', 'toys', 'games', 'books', 'bedding', 'weightedBlanket']
        for field in generalFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'general'}




class donorForm(ModelForm):
    class Meta:
        model = donorEntry
        fields = ('name', 'emailAddress', 'mailingAddress', 'itemsDonated')


    def __init__(self, *args, **kwargs):        
        super(donorForm, self).__init__(*args, **kwargs)
        
        self.fields['name'].label = "Donor's Name: *"
        self.fields['emailAddress'].label = "Donor Email Address: *"
        self.fields['mailingAddress'].label = "Donor Mailing Address: *"
        self.fields['itemsDonated'].label = "General Type of Item(s) Donated: *"

        for aField in self.fields.keys():
            self.fields[aField].initial = ''



class hoursForm(ModelForm):
    class Meta:
        model = hoursEntry
        fields = ('date', 'hoursWorked')


    def __init__(self, *args, **kwargs):        
        super(hoursForm, self).__init__(*args, **kwargs)
        self.fields['date'].input_formats = ['%m/%d/%Y']

        for one in ['date', 'hoursWorked']:
            self.fields[one].label = processName(one) + ": *"

        self.fields['date'].initial = hoursEntry._meta.get_field('date').get_default().strftime('%m/%d/%Y')


        