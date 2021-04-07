from django import forms
from .models import Donate

class NewDonateForm(forms.ModelForm):

    class Meta:
        model =Donate
        fields =['value']
