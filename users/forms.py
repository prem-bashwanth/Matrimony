from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField()
    
    class Meta:
        model =User
        fields=['username','email','password1','password2']
class profile_updation_form1(forms.ModelForm):
    # dob = forms.DateField(
    #     widget=forms.DateInput(attrs={'type': 'date'}),
    #     required=True
    # )
    height = forms.FloatField(required=True)
    weigth = forms.FloatField(required=True)
    
    
    class Meta:
        model =profile_personal_info
        fields=['firstname','lastname','image_pic','image1','image2','image3','city','state','dob','height','diet','gender','weigth','blood_group','physical_disability','skin_colour',
                'marital_status','phone_number']

class profile_updation_form2(forms.ModelForm):
    income = forms.IntegerField(required=True)
    class Meta:
        model =profile_educational_and_career_info
        fields=['qualification','collage_name','occupation','company_name','income']

class profile_updation_form3(forms.ModelForm):
    class Meta:
        model =profile_family_details
        fields=['fathers_occupation','mothers_occupation','religion','caste','mothertounge']
class profile_updation_form4(forms.ModelForm):
    agemin = forms.IntegerField(required=True)
    agemax = forms.IntegerField(required=True)
    income = forms.IntegerField(required=True)
    height = forms.IntegerField(required=True)
    class Meta:
        model =partner_preferences
        fields=['agemin','agemax','marital_status','religion','height','caste','mothertounge','occupation','qualificaton','income','country']
    
    
    
    
            
            
        