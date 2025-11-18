from django import forms
from django.forms import ModelForm
from .models import Book, Rating, Review, Message   


#class BookForm(ModelForm):
#    class Meta:
#        model = Book
#        fields = [
#            'name',
#            'web',
#            'price',
#            'picture',
#        ]


class RatingForm(ModelForm):
    value = forms.IntegerField(
        label = 'Your Rating (1-5)',
        min_value = 1,
        max_value = 5,
        widget = forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a number between 1 and 5'
        })
    )
    
    class Meta:
        model = Rating
        fields = ['value']

#---------------------------- ADDED ----------------------------#
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["name", "web", "price", "picture"]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book name'}),
            'web': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(ModelForm):
    rating = forms.IntegerField(
        min_value=1, 
        max_value=5, 
        help_text="Rate 1–5",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '1-5'})
    )
    
    def __init__(self, *args, **kwargs):
        user=None
        if 'user' in kwargs:
            user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        if user is not None and user.is_authenticated:
            self.fields['reviewer_name'].required = False
            self.fields['reviewer_name'].widget = forms.HiddenInput()
        # Add Bootstrap classes to fields
        self.fields['reviewer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['comment'].widget.attrs.update({'class': 'form-control', 'rows': 4})
    
    class Meta:
        model = Review
        fields = ["reviewer_name", "rating", "comment"]

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "body"]

class SearchForm(forms.Form):
    q = forms.CharField(
        label="Search", 
        required=False, 
        widget=forms.TextInput(attrs={
            "placeholder": "Search by book name or website", 
            "class": "form-control",
            "size": 32
        })
    )