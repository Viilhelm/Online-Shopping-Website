from django import forms
from .models import OrderItem


class ReviewForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['myRate', 'myComment']