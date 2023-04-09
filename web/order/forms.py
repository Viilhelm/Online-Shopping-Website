from django import forms
from .models import OrderItem

class RRAddForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields= ['myComment']
        widgets={
            'myComment':forms.Textarea(attrs={'class':'form-control'}),

        }
        labels = {'myComment': 'My Comment'}