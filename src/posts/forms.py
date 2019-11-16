from django import forms
from .models import ProblemPost, GeneralPost, Comment, ExamplePost
from django.core.exceptions import ValidationError
import os


class ExampleForm(forms.ModelForm):
    class Meta:
        model = ExamplePost
        fields = '__all__'


class PostForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}))

    class Meta:
        model = GeneralPost
        fields = ['title', 'description', 'image']

    def clean_description(self):
        desc = self.cleaned_data.get('description')
        if len(desc) < 10:
            raise ValidationError("Description too short")
        return desc


class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label='', widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'your comment here...'}))

    class Meta:
        fields = ('body',)
        model = Comment
