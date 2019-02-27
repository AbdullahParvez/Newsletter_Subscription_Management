from django import forms
from .models import Post, Rating


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')

        widgets = {
            'title': forms.TextInput(),
            'text': forms.Textarea()
        }


class RatingForm(forms.Form):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    email = forms.EmailField()
    rating = forms.ChoiceField(choices=RATING_CHOICES)


class SubscriberForm(forms.Form):
    email = forms.EmailField()
