from django import forms
from .models import Category

class NewCategoryForm(forms.ModelForm):

    class Meta:
        model =Category
        fields =['name']
