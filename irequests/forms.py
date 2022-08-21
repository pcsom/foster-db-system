from dataclasses import field
import json
from django.forms import CharField, ModelForm

from mainpg.models import ReqFormSettings
from utility import deProcessName
from .models import itemsRequest, processName
from accounts.models import child
from django import forms



# class itemsRequestForm(ModelForm):
#     class Meta:
#         model = itemsRequest
#         fields = ('forChild',
            
#             'onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
#             'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 'strollerType',
#             'formula', 'formulaType', 'diapers', 'diapersSize', 'wipes', 'otherInfantNeeds', 

#             'shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
#             'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'holidayOutfit', 'shoes', 

#             'toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 'ethnicHairCareProducts', 
#             'hairAccessories', 'makeUpItems', 'makeUpItemsDescription',
            
#             'schoolSupplies', 'toysGamesBooks', 'bedding', 'weightedBlanket', 'otherNeeds')
    


#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('parentUser')
        
#         super(itemsRequestForm, self).__init__(*args, **kwargs)
        
#         #Child
#         self.fields['forChild'].label = "Please select the child you are making a request for."
#         self.fields['forChild'].queryset = child.objects.filter(parent=self.user)


#         #THE FOLLOWING FIELD NAMES ARE REFERENCED, AND HARD-CODED, IN THE HTML FILE TO MAKE A NEW REQUEST
#         #Infants
#         infantFields = ['onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
#             'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 'strollerType',
#             'formula', 'formulaType', 'diapers', 'diapersSize', 'wipes', 'otherInfantNeeds']
#         for field in infantFields:
#             self.fields[field].label = processName(field)
#             self.fields[field].widget.attrs = {'class': 'infant'}
        
#         self.fields['strollerType'].choices = [('single', 'Single'), ('double', 'Double')]
#         self.fields['otherInfantNeeds'].label = "Please describe any other infant needs."


#         #Child/teen
#         childFields = ['shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
#             'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'holidayOutfit', 'shoes']
#         for field in childFields:
#             self.fields[field].label = processName(field)
#             self.fields[field].widget.attrs = {'class': 'child'}


#         #Toiletries
#         toiletriesFields = ['toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 
#             'ethnicHairCareProducts', 'hairAccessories', 'makeUpItems', 'makeUpItemsDescription']
#         for field in toiletriesFields:
#             self.fields[field].label = processName(field)
#             self.fields[field].widget.attrs = {'class': 'toiletries'}
        
#         self.fields['makeUpItemsDescription'].label = "Please describe the needed make-up items."


#         #General Fields
#         generalFields = ['schoolSupplies', 'toysGamesBooks', 'bedding', 'weightedBlanket', 
#             'otherNeeds']
#         for field in generalFields:
#             self.fields[field].label = processName(field)
#             self.fields[field].widget.attrs = {'class': 'general'}

#         self.fields['schoolSupplies'].label = "Please list any needed school supplies."
#         self.fields['toysGamesBooks'].label = "Please list any needed toys, games, or books."
#         self.fields['bedding'].label = "Please list any needed bedding items."
#         self.fields['otherNeeds'].label = "Please list any other needs."





class itemsRequestForm(forms.Form):

    forChild = forms.ModelChoiceField(queryset=child.objects.all(), required=True, empty_label=None)
    
    # STROLLER_TYPE = (
    #     ('double', 'Double'),
    #     ('single', 'Single'),
    # )

    

    # #Infant items
    # onesies = forms.BooleanField(required=False)
    # twoPieceOutfits = forms.BooleanField(required=False)
    # sleepSack = forms.BooleanField(required=False)
    # cribSheets = forms.BooleanField(required=False)
    # crib = forms.BooleanField(required=False)
    # bibs = forms.BooleanField(required=False)
    # receivingBlankets = forms.BooleanField(required=False)
    # burpCloths = forms.BooleanField(required=False)
    # washcloths = forms.BooleanField(required=False)
    # bottles = forms.BooleanField(required=False)
    # stroller = forms.BooleanField(required=False)
    # strollerType = forms.CharField(required=False, max_length=7)
    # formula = forms.BooleanField(required=False)
    # formulaType = forms.CharField(required=False, max_length=100)
    # diapers = forms.BooleanField(required=False)
    # diapersSize = forms.CharField(required=False, max_length=100)
    # wipes = forms.BooleanField(required=False)
    # otherInfantNeeds = forms.CharField(required=False, widget=forms.Textarea)

    # #Children/teen
    # shortSleeveShirts = forms.BooleanField(required=False)
    # longSleeveShirts = forms.BooleanField(required=False)
    # shorts = forms.BooleanField(required=False)
    # longPants = forms.BooleanField(required=False)
    # pajamas = forms.BooleanField(required=False)
    # dressClothes = forms.BooleanField(required=False)
    # dresses = forms.BooleanField(required=False)
    # winterCoats = forms.BooleanField(required=False)
    # swimwear = forms.BooleanField(required=False)
    # holidayOutfit = forms.BooleanField(required=False)
    # shoes = forms.BooleanField(required=False)

    # #Toiletries
    # toothbrush = forms.BooleanField(required=False)
    # toothpaste = forms.BooleanField(required=False)
    # deodorant = forms.BooleanField(required=False)
    # soap = forms.BooleanField(required=False)
    # shampoo = forms.BooleanField(required=False)
    # ethnicHairCareProducts = forms.BooleanField(required=False)
    # hairAccessories = forms.BooleanField(required=False)
    # makeUpItems = forms.BooleanField(required=False)
    # makeUpItemsDescription = forms.CharField(required=False, widget=forms.Textarea)
    
    # #School Supplies
    # schoolSupplies = forms.CharField(required=False, widget=forms.Textarea)

    # #Toys/Games/Books
    # toysGamesBooks = forms.CharField(required=False, widget=forms.Textarea)

    # #Bedding Furniture/items
    # bedding = forms.CharField(required=False, widget=forms.Textarea)

    # #Weighted Blanket
    # weightedBlanket = forms.BooleanField(required=False)

    # #Other needs
    # otherNeeds = forms.CharField(required=False, widget=forms.Textarea)
    

    #Dynamic strat - in each init call, it pulls from the dic in the reqFormSettings singleton
    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('parentUser')
        
        super(itemsRequestForm, self).__init__(*args, **kwargs)
        
        #Child
        self.fields['forChild'].label = "Please select the child you are making a request for."
        self.fields['forChild'].queryset = child.objects.filter(parent=self.user)

        sett = ReqFormSettings.load()
        databaseDisplay = sett.databaseDisplay
        for group in sett.fieldInfo:
            for fieldInfo in group[1]:
                dbn = fieldInfo[0]
                dsp = databaseDisplay[dbn]
                dtype = fieldInfo[1]
                dropOps = None
                if dtype == 'dropdown':
                    dropOps = fieldInfo[2]

                if dtype == "boolean":
                    self.fields[dbn] = forms.BooleanField()
                    self.fields[dbn].initial = False
                elif dtype == "char":
                    self.fields[dbn] = forms.CharField()
                    self.fields[dbn].initial = ""
                elif dtype == "textarea":
                    self.fields[dbn] = forms.CharField()
                    self.fields[dbn].initial = ""
                    self.fields[dbn].widget = forms.Textarea()
                elif dtype == "dropdown":
                    curChoice = tuple([(deProcessName(x), x) for x in dropOps])
                    self.fields[dbn] = forms.CharField()
                    #self.fields[dbn].choices = curChoice
                    self.fields[dbn].widget = forms.Select(choices=curChoice)
                    
                    #print(dbn)
                    #print(curChoice)
                    #self.fields[dbn].widget = forms.RadioSelect(choices=curChoice)
                
                self.fields[dbn].label = dsp
                self.fields[dbn].required = False
                self.fields[dbn].widget.attrs = {'data-itemtype': group[0], 'class': 'formfield'}

        #print(self.fields)



        """
        self.user = kwargs.pop('parentUser')
        
        super(itemsRequestForm, self).__init__(*args, **kwargs)
        
        #Child
        self.fields['forChild'].label = "Please select the child you are making a request for."
        self.fields['forChild'].queryset = child.objects.filter(parent=self.user)


        #THE FOLLOWING FIELD NAMES ARE REFERENCED, AND HARD-CODED, IN THE HTML FILE TO MAKE A NEW REQUEST
        #Infants
        self.fields['infantTest'] = forms.BooleanField()
        infantFields = ['onesies', 'twoPieceOutfits', 'sleepSack', 'cribSheets', 'crib', 'bibs',  
            'receivingBlankets', 'burpCloths', 'washcloths', 'bottles', 'stroller', 'strollerType',
            'formula', 'formulaType', 'diapers', 'diapersSize', 'wipes', 'otherInfantNeeds', 'infantTest']
        for field in infantFields:
            self.fields[field].label = processName(field)
            self.fields[field].initial = False
            self.fields[field].widget.attrs = {'class': 'infant'}
        
        self.fields['strollerType'].choices = [('single', 'Single'), ('double', 'Double')]
        self.fields['otherInfantNeeds'].label = "Please describe any other infant needs."


        #Child/teen
        childFields = ['shortSleeveShirts', 'longSleeveShirts', 'shorts', 'longPants', 'pajamas', 
            'dressClothes', 'dresses', 'winterCoats', 'swimwear', 'holidayOutfit', 'shoes']
        for field in childFields:
            self.fields[field].label = processName(field)
            self.fields[field].initial = False
            self.fields[field].widget.attrs = {'class': 'child'}


        #Toiletries
        toiletriesFields = ['toothbrush', 'toothpaste', 'deodorant', 'soap', 'shampoo', 
            'ethnicHairCareProducts', 'hairAccessories', 'makeUpItems', 'makeUpItemsDescription']
        for field in toiletriesFields:
            self.fields[field].label = processName(field)
            self.fields[field].initial = False
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
        self.fields['weightedBlanket'].initial = False

        blankDesc = ['formulaType', 'diapersSize', 'strollerType', 'otherInfantNeeds', 'makeUpItemsDescription']
        for field in blankDesc:
            self.fields[field].initial = ""

        #print(self.fields)
        """




def formToReqModel(form):
    cur = itemsRequest()
    dat = {}
    cleaned = form.cleaned_data
    for i in cleaned:        
        if cleaned[i] not in [False, "", None] and i!="forChild":
            dat[i] = cleaned[i]
    cur.forChild = cleaned['forChild']
    cur.formData = json.dumps(dat)
    return cur




# def formToReqModel(form):
#     cur = itemsRequest()
#     dat = {}
#     cleaned = form.cleaned_data
#     for i in cleaned:
#         print(i, cleaned[i])
        
#         if not (isinstance(cleaned[i], str) and cleaned[i]) and i!="forChild":
#             dat[i] = cleaned[i]
#             print("pass")
#     cur.forChild = cleaned['forChild']
#     cur.formData = json.dumps(dat)
#     return cur

            





# def getReqFormFields(strDate=False):
    
#     allfields = [(processName(field.name), getattr(self, field.name)) for field in itemsRequestForm.declared_fields.keys()]
#     theDate = self.date
#     if strDate:
#         theDate = str(theDate)
#     finalfields = {"name": self.__str__(), "childDateInfo": self.childDateInfo(), "receiving": allfields[3][1], "date": theDate, "fields": []}
#     for name, value in allfields[6:]:
#         if value and value != 'False':
#             newVal = ": " + str(value)
#             if newVal == ': True':
#                 newVal = " "
#             finalfields['fields'].append((name, newVal))

#     return finalfields

