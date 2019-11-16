from .models import Profile
from django import forms


class ProfileModelForm(forms.ModelForm):
    bio = forms.CharField(label="Bio", widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Few words about you',
            'rows': 3,
        }))
    website = forms.CharField(label="Website", required=False, widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Your website',
        }))

    class Meta:
        model = Profile
        fields = ('bio', 'website', 'profile_picture',)
