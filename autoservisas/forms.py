from .models import OrderReview
from django import forms

class OrderReviewForm(forms.ModelForm):
    class Meta:
        model = OrderReview
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'placeholder': 'Rašykite savo atsiliepimą čia...'})
        }