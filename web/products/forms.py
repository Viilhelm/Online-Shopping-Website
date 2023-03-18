from django import forms
from .models import Product

class ProductsAddForm(forms.ModelForm):
    class Meta:
        model = Product
        fields= ['productName','price','ISBN','author','publisher','introduction','image','category']
        widgets={
            'productName':forms.TextInput(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'ISBN':forms.TextInput(attrs={'class':'form-control'}),
            'author':forms.TextInput(attrs={'class':'form-control'}),
            'publisher':forms.TextInput(attrs={'class':'form-control'}),
            'introduction':forms.TextInput(attrs={'class':'form-control'}),
            'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
            'catgegory':forms.Select(attrs={'class':'form-control'}),

        }