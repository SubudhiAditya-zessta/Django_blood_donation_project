from django import forms
from .models import Donor,BloodBank

class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['donor_name', 'donor_phone']
    
   


