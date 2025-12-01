from django import forms
from django.forms import ModelForm
from .models import Book, Review, Message

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "isbn"]

class ReviewForm(ModelForm):
    rating = forms.IntegerField(min_value=1, max_value=5, help_text="Rate 1–5")
    class Meta:
        model = Review
        fields = ["reviewer_name", "rating", "comment"]

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ["name", "email", "body"]

class SearchForm(forms.Form):
    q = forms.CharField(label="Search", required=False, widget=forms.TextInput(
        attrs={"placeholder": "Title, author, or ISBN", "size": 32}
    ))
