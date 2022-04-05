from django.forms import ModelForm
from .models import itemsRequest, processName
from accounts.models import child



class itemsRequestForm(ModelForm):
    class Meta:
        model = itemsRequest
        fields = ('forChild',
            
            'onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
            'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 'strollerType',
            'formula', 'formulaType', 'diapers', 'diapersSize', 'wipes', 'otherInfantNeeds', 

            'shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
            'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'holidayOutfit', 'shoes', 

            'toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 'ethnicHairCareProducts', 
            'hairAccessories', 'makeUpItems', 'makeUpItemsDescription',
            
            'schoolSupplies', 'toysGamesBooks', 'bedding', 'weightedBlanket', 'otherNeeds')
    


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('parentUser')
        
        super(itemsRequestForm, self).__init__(*args, **kwargs)
        
        #Child
        self.fields['forChild'].label = "Please select the child you are making a request for."
        self.fields['forChild'].queryset = child.objects.filter(parent=self.user)


        #THE FOLLOWING FIELD NAMES ARE REFERENCED, AND HARD-CODED, IN THE HTML FILE TO MAKE A NEW REQUEST
        #Infants
        infantFields = ['onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
            'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 'strollerType',
            'formula', 'formulaType', 'diapers', 'diapersSize', 'wipes', 'otherInfantNeeds']
        for field in infantFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'infant'}
        
        self.fields['strollerType'].choices = [('single', 'Single'), ('double', 'Double')]
        self.fields['otherInfantNeeds'].label = "Please describe any other infant needs."


        #Child/teen
        childFields = ['shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
            'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'holidayOutfit', 'shoes']
        for field in childFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'child'}


        #Toiletries
        toiletriesFields = ['toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 
            'ethnicHairCareProducts', 'hairAccessories', 'makeUpItems', 'makeUpItemsDescription']
        for field in toiletriesFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'toiletries'}
        
        self.fields['makeUpItemsDescription'].label = "Please describe the needed make-up items."


        #General Fields
        generalFields = ['schoolSupplies', 'toysGamesBooks', 'bedding', 'weightedBlanket', 
            'otherNeeds']
        for field in generalFields:
            self.fields[field].label = processName(field)
            self.fields[field].widget.attrs = {'class': 'general'}

        self.fields['schoolSupplies'].label = "Please list any needed school supplies."
        self.fields['toysGamesBooks'].label = "Please list any needed toys, games, or books."
        self.fields['bedding'].label = "Please list any needed bedding items."
        self.fields['otherNeeds'].label = "Please list any other needs."




