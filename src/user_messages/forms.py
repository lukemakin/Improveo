from django import forms
from .models import Message


class MessageModelForm(forms.ModelForm):
    body = forms.CharField(required=True, label='Message', widget=forms.Textarea(attrs={
        'rows': 5,
    }))
    class Meta:
        model = Message
        exclude = ('read_author', 'read', 'new', 'message_from', 'answers', 'main',)


class MessageAnswerModelForm(forms.ModelForm):
    body = forms.CharField(required=False, label='Respond to the message', widget=forms.Textarea(attrs={
        'rows': 3,
    }))

    class Meta:
        model = Message
        fields = ('body',)
